#!/bin/bash

rm db.sqlite3
cd medsApp/migrations
rm 000*
rm -r __p*
cd ../..
./migrate.sh
cd ../parsing
./import.sh
