#!/bin/bash
wget https://fsrar.gov.ru/opendata/7710747640-reestr/data-20211001t0000-structure-20190918t0000.zip --no-check-certificate
unzip data-20211001t0000-structure-20190918t0000.zip
mv data-20211001t0000-structure-20190918t0000.xml lic.xml
rm data-20211001t0000-structure-20190918t0000.zip
dropdb alkolic
createdb alkolic
psql -d alkolic < createTableLics.sql
./uploadlics.py
rm lic.xml
