#!/bin/sh

psql --version
if [ "$?" -gt "0" ]; then
  echo "PostgreSql not installed, please install before proceeding"
else
  echo "PostgreSQL installed"
fi

python -c "import psycopg2; print(psycopg2.__version__)"
if [ "$?" -gt "0" ]; then
  sudo pip install psycopg2
else
  echo "psycopg2 installed"
fi

if [ "$1" == "-create_db" ];then
    createuser -P -s -e scott
    python createdb.py
    python manage.py syncdb --noinput
    python manage.py sql scottviz_app
    python manage.py syncdb --noinput
elif [ "$1" == "-drop_db" ];then
    dropdb 'flowerpower'
elif [ "$1" == "-populate_test" ];then
    python populate_test_data.py
    python manage.py syncdb --noinput
elif [ "$1" == "-populate" ];then
    python populate_test_data.py
    python manage.py syncdb --noinput
else
    echo "Usage: -create_db\n -populate_test\n -populate\n -drop_db\n "
fi