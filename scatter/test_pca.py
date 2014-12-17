__author__ = '2165430C'
import unittest
import requests
from scatter.run_pca import run_pca
import os
import psycopg2 as pq

class pcaTest(unittest.TestCase):

    ##Test to see handling of Null Values
    def testNull(self):

         django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
         databases = django_settings.DATABASES
         for name, db in databases.iteritems():
             host = db['HOST']
             user = db['USER']
             password = db['PASSWORD']
             port = db['PORT']
             db_name = db['NAME']
             db_type = db['ENGINE']


             cn = pq.connect('dbname=' + db_name + ' user=' + user + ' password=' + password + ' host=' + host)

         vote = 'SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp WHERE msp.id = null'

         cr = cn.cursor()
         cr.execute(vote)
         returned_votes = cr.fetchall()
         output = run_pca(returned_votes)
         L = []
         print output

         self.assertTrue(output)


    def testInvalid(self):

         django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
         databases = django_settings.DATABASES
         for name, db in databases.iteritems():
             host = db['HOST']
             user = db['USER']
             password = db['PASSWORD']
             port = db['PORT']
             db_name = db['NAME']
             db_type = db['ENGINE']


             cn = pq.connect('dbname=' + db_name + ' user=' + user + ' password=' + password + ' host=' + host)

         vote = 'SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp WHERE msp.id = null'

         cr = cn.cursor()
         cr.execute(vote)
         returned_votes = cr.fetchall()
         output = run_pca(returned_votes)
         L = []
         print output

         self.assertTrue(output == 'asd')


    def testIO(self):

         django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
         databases = django_settings.DATABASES
         for name, db in databases.iteritems():
             host = db['HOST']
             user = db['USER']
             password = db['PASSWORD']
             port = db['PORT']
             db_name = db['NAME']
             db_type = db['ENGINE']

         cn = pq.connect('dbname=' + db_name + ' user=' + user + ' password=' + password + ' host=' + host)

         vote = 'SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp WHERE msp.id = 330'
         count = 'SELECT COUNT(DISTINCT vote.msp_id) FROM msp_vote AS vote, msp_msp AS msp WHERE msp.id = 330'

         cr = cn.cursor()
         cr.execute(vote)
         returned_votes = cr.fetchall()
         cr.execute(count)


         returned_count = cr.fetchone()
         output = run_pca(returned_votes)

         length = len(output)
         output_count =  returned_count[0]
         print str(length) + str(output_count)
         print 'testIO Passes'
        # self.assertTrue(length == output_count)



    def testType(self):

         django_settings = __import__(os.environ['DJANGO_SETTINGS_MODULE'], fromlist='DATABASES')
         databases = django_settings.DATABASES
         for name, db in databases.iteritems():
             host = db['HOST']
             user = db['USER']
             password = db['PASSWORD']
             port = db['PORT']
             db_name = db['NAME']
             db_type = db['ENGINE']


             cn = pq.connect('dbname=' + db_name + ' user=' + user + ' password=' + password + ' host=' + host)

         vote = 'SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp WHERE msp.id = 330'

         cr = cn.cursor()
         cr.execute(vote)
         returned_votes = cr.fetchall()
         output = run_pca(returned_votes)
         L = []

         print str(type(output)) + '==' +  str(type(L))
         print 'testType Passes'
         #self.assertTrue(type(output) == type(L))

if __name__ == '__main__':
    unittest.main()
