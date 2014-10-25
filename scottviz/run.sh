#!/bin/sh
createuser -P -s -e scott
python createdb.py
python manage.py syncdb --noinput
python manage.py sql scottviz_app
python manage.py syncdb --noinput
python populate_test_data.py
