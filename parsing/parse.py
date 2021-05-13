import sys
import re
import pandas as pd
from sqlalchemy import create_engine

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

def main(xlfile, date, db, table_name):
    df_dict = pd.read_excel(xlfile, sheet_name=None)
    for sh in ['A1', 'A2', 'A3', 'B', 'C']:
        # LP, Termin decyzji, Okres obowiązywania
        df_dict[sh].drop(columns=df_dict[sh].columns[[0, 5, 6]], inplace=True)

    for sh in ['D', 'E']:
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

    for sh in ['D', 'E']:
        with open(sh + '.txt', 'r') as f:
            df_dict[sh]['registered_funding'] = f.read()
        df_dict[sh]['payment_lvl'] = 'bezpłatny do limitu'
        df_dict[sh]['patient_payment'] = 0

    for df in df_dict.values():
        df.to_sql(table_name, con=create_engine('sqlite:///' + db), if_exists='append', index=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 4:
        exit("Usage: python3 parse.py path/to/spreadsheet.xlsx YYYYMMDD /absolute/path/to/sqlite/db db_name")

    sys.exit(main(args[0], args[1], args[2], args[3]))
