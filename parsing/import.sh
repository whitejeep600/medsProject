#!/bin/bash

rm xd.xlsx

for f in *.xlsx
do
    echo 'processing' $f
    cp $f xd.xlsx
    python3 delete.py xd.xlsx
    python3 parse.py xd.xlsx ${f%.xlsx} ~/studia/sem4/IO/medsProject/medsProject/db.sqlite3 medsApp_drug medsApp_drugkey
    rm xd.xlsx
done
