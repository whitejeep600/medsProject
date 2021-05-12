import sys
# from pandas import read_excel
import pandas as pd
from sqlalchemy import create_engine

def main(xlfile, db, table_name):
    df_dict = pd.read_excel(xlfile, sheet_name=None)
    for sh in ['A1', 'A2', 'A3', 'B', 'C']:
        # LP, Termin decyzji, Okres obowiązywania
        df_dict[sh].drop(columns=df_dict[sh].columns[[0, 5, 6]], inplace=True)

    for sh in ['D', 'E']:
        # LP
        df_dict[sh].drop(columns=df_dict[sh].columns[[0]], inplace=True)

    # TODO
    # Rozbicie Nazwa postać i dawka leku na nazwę, postać i dawkę.
    # Dodać kolumnę 'date'.

    for df in df_dict.values():
        df.rename(columns={
            'Substancja czynna': 'active_substance',
            'Nazwa  postać i dawka': 'MED', # TODO
            'Nazwa  postać i dawka leku': 'MED', # TODO
            'Nazwa i postać leku': 'MED', # TODO
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

    for df in df_dict.values():
        df.to_sql(table_name, con=create_engine('sqlite:///' + db), if_exists='append', index=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 3:
        exit("Usage: python3 parse.py path/to/spreadsheet.xlsx /absolute/path/to/sqlite/db db_name")

    sys.exit(main(args[0], args[1], args[2]))
