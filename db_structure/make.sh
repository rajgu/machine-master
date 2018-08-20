#!/bin/bash

echo '|-------------------------------------|'
echo "|  Welcome to STP-master DB Maker!!!  |"
echo '|-------------------------------------|'


dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
dbname=$1

if [ -z $dbname ]; then

	if [ ! -f "$dir/../config.ini" ]; then
		echo "Glowny plik konfiguracyjny nie istnieje!!!"
		exit 1
	fi

	dbname=$(cat $dir/../config.ini | grep  -A 1 '\[database\]' | grep 'name' | awk '{print $2}')
fi

if [ -z $dbname ]; then
	echo "Nie udalo mi sie odczytac nazwy bazy danych z pliku konfiguracyjnego"
	exit 1
fi

echo "Tworze baze danych: '$dbname'"

for sql_file in `ls $dir | grep -E '^Types' | grep -E '\.sql$'`; do
	echo "Przetwarzam plik: ${sql_file}"
	sqlite3 "${dir}/../${dbname}" < "${dir}/${sql_file}"
done
for sql_file in `ls $dir | grep -vE '^Types' | grep -E '\.sql$'`; do
	echo "Przetwarzam plik: ${sql_file}"
	sqlite3 "${dir}/../${dbname}" < "${dir}/${sql_file}"
done