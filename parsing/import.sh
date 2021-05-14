#!/bin/bash

for f in '20210101' '20210301'
do
    cp ${f}.xlsx xd.xlsx
    python3 delete.py xd.xlsx
    python3 parse.py xd.xlsx $f ~/studia/sem4/IO/medsProject/medsProject/db.sqlite3 medsApp_drug
done
