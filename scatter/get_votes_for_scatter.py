__author__ = '2168879m'
import os
import psycopg2 as pq

def get_votes_for_scatter(parties,topics):

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
    cr = cn.cursor()
    print parties
    print topics

    len_parties = len(parties)
    len_topics = len(topics)

    if len_parties and len_topics:
        # filter by both
        print "not yet"
    elif len_parties:
        # filter by party
        print "parties"
        isFirst = True
        count = 0
        votes = "SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp "
        while count < len_parties:
            print parties[count]
            if isFirst == 1:
                votes = votes + "WHERE (msp.party_id = " + parties[count]
                isFirst = False
            else:
                votes = votes + " OR msp.party_id = " + parties[count]
            count += 1
        votes = votes + ") AND (vote.msp_id = msp.id) ORDER BY vote.msp_id"
        print votes
    elif len_topics:
        #filter by topics
        print "topics"
        isFirst = True
        count = 0
        votes = "SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_division AS div "
        while count < len_topics:
            if isFirst == 1:
                votes = votes + "WHERE (div.topic_id = " + topics[count]
                isFirst = False
            else:
                votes = votes + " OR div.topic_id = " + topics[count]
            count += 1
        votes = votes + ") AND (vote.division_id = div.id) ORDER BY vote.msp_id"
        print votes
    else:
        # no filter
        print "no filter"
        votes = "SELECT DISTINCT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote ORDER BY msp_id"

    cr.execute(votes)
    returned_votes = cr.fetchall()
    print len(returned_votes)

    return returned_votes