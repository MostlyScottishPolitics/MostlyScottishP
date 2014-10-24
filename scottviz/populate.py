import os
import time
import psycopg2

def create_db():
    deadline = time.time() + 60
    while time.time() < deadline:
        try:
            print("creating database")
            django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
            databases = django_settings.DATABASES
            for name, db in databases.iteritems():
                host = db['HOST']
                user = db['USER']
                password = db['PASSWORD']
                port = db['PORT']
                db_name = db['NAME']
                db_type = db['ENGINE']
                if db_type.endswith('postgresql_psycopg2'):
                    print 'creating database %s on %s' % (db_name, host)
                    con = psycopg2.connect(host=host, user=user, password=password, port=port, database='postgres')
                    con.set_isolation_level(0)
                    cur = con.cursor()
                    try:
                        cur.execute('CREATE DATABASE %s' % db_name)
                    except psycopg2.ProgrammingError as detail:
                        print detail
                    exit(0)
                else:
                    print("ERROR: {0}".format(db_type))
                    exit(1)
        except psycopg2.OperationalError:
            print "Could not connect to the database, retry in 10 seconds"
            time.sleep(10)


    print 'Something is wrong.'
    exit(1)
#def populate_db():

if __name__ == '__main__':
    import sys
    create_db()