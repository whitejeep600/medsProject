import sys
import re
import pandas as pd
from sqlalchemy import *
from sqlalchemy import schema

# assumes there are no commas in med_name,
# no commas in dose if there is no '0,' in dose
def split_med(x):
    frst = x.find(',')
    if frst == -1:
        return [x.strip()]
    # list of delimitting indices
    indices = [0, frst]
    # check where dose part can start
    matchobj = re.compile(r'0,\d').search(x)
    ambiguous = matchobj.start() + 1 if matchobj else -1
    if ambiguous == -1:
        # if no 0,\d present then assume no commas in dose
        tmp = x.rfind(',')
        if tmp != indices[1]:
            indices.append(tmp)
    else:
        tmp = x.rfind(',', indices[1], ambiguous)
        if tmp != -1:
            indices.append(tmp)
    indices.append(None)
    return [x[indices[i]:indices[i + 1]].strip(' ,') for i in range(len(indices) - 1)]

def main(xlfile, date, db, drug_table, key_table):
    df_dict = pd.read_excel(xlfile, sheet_name=None, dtype=object)
    for sh in ['A1', 'A2', 'A3', 'B', 'C']:
        # LP, Termin decyzji, Okres obowiązywania
        df_dict[sh].drop(columns=df_dict[sh].columns[[0, 5, 6]], inplace=True)

    for sh in ['D', 'E']:
        if sh in df_dict:
            # LP
            df_dict[sh].drop(columns=df_dict[sh].columns[[0]], inplace=True)

    for key, df in df_dict.items():
        # rename columns for database and normalise "nazwa postać dawka" to "med" to split it
        df.rename(columns={
            'Substancja czynna': 'active_substance',
            'Nazwa  postać i dawka': 'med',
            'Nazwa  postać i dawka leku': 'med',
            'Nazwa i postać leku': 'med',
            'Zawartość opakowania': 'pack_size',
            'Numer GTIN lub inny kod jednoznacznie identyfikujący produkt': 'gtin',
            'Kod EAN lub inny kod odpowiadający kodowi EAN': 'gtin',
            'Grupa limitowa': 'limit_group',
            'Urzędowa cena zbytu': 'official_price',
            'Cena hurtowa brutto' : 'wholesale_price',
            'Cena detaliczna': 'retail_price',
            'Wysokość limitu finansowania': 'refund_limit',
            'Zakres wskazań objętych refundacją': 'registered_funding',
            'Zakres wskazań pozarejestracyjnych objętych refundacją': 'nonregistered_funding',
            'Poziom odpłatności': 'payment_lvl',
            'Wysokość dopłaty świadczeniobiorcy': 'patient_payment',
            'Oznaczenie załącznika zawierającego zakres wskazań objętych refundacją  wg ICD 10 ': 'registered_funding'
        }, inplace=True)
        df['date'] = pd.to_datetime(date, format='%Y%m%d')
        # Split 'med' column.
        tmp = df['med'].apply(lambda x: pd.Series(split_med(str(x)))).rename(columns={
            0: 'med_name',
            1: 'med_form',
            2: 'dose'
        })
        df.drop(columns=['med'], inplace=True)
        df_dict[key] = pd.concat([df, tmp], axis=1)

    # Add lacking columns to some sheets.
    for sh in ['D', 'E']:
        if sh in df_dict:
            with open(sh + '.txt', 'r') as f:
                df_dict[sh]['registered_funding'] = f.read()
            df_dict[sh]['payment_lvl'] = 'bezpłatny do limitu'
            df_dict[sh]['patient_payment'] = '0,00'

    # Change column types for to_sql() to work.
    for key in df_dict:
        for x in ['patient_payment', 'official_price', 'wholesale_price', 'retail_price', 'refund_limit']:
            try:
                df = df_dict[key]
                df[x] = df[x].apply(lambda y: float(y.split()[0].replace(',', '.')))
                df_dict[key] = df
            except:
                pass

    key_dict = {}
    for sh in ['A1', 'A2', 'A3', 'B', 'C']:
        if 'nonregistered_funding' in df_dict[sh].columns.values.tolist():
            key_dict[sh] = df_dict[sh][['gtin', 'registered_funding', 'nonregistered_funding']]
            df_dict[sh].drop(['gtin', 'registered_funding', 'nonregistered_funding'], axis=1, inplace=True)
        else:
            key_dict[sh] = df_dict[sh][['gtin', 'registered_funding']]
            df_dict[sh].drop(['gtin', 'registered_funding'], axis=1, inplace=True)

    engine = create_engine('sqlite:///' + db)
    keys = Table(key_table, MetaData(), autoload=True, autoload_with=engine)
    drugs = Table(drug_table, MetaData(), autoload=True, autoload_with=engine)
    with engine.connect() as conn:
        for df, key in zip(df_dict.values(), key_dict.values()):
            for a, b in zip(df.iterrows(), key.iterrows()):
                tmp_dict = b[1].to_dict()
                com = select(keys.c.id).where(keys.c.gtin == tmp_dict['gtin']).where(keys.c.nonregistered_funding == tmp_dict.get('nonregistered_funding', None)).where(keys.c.registered_funding == tmp_dict['registered_funding'])
                result = conn.execute(com).first()
                key_id = result[0] if result else conn.execute(
                        insert(keys),
                        tmp_dict
                    ).inserted_primary_key[0]

                tmp = a[1].to_dict()
                tmp['key_id'] = key_id
                conn.execute(
                    insert(drugs),
                    tmp
                )


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 5:
        exit("Usage: python3 parse.py path/to/spreadsheet.xlsx YYYYMMDD /absolute/path/to/sqlite/db drug_table_db_name key_table_db_name")

    sys.exit(main(args[0], args[1], args[2], args[3], args[4]))
