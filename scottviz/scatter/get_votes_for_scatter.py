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

    any_parties = len(parties)
    any_topics = len(topics)

    if any_parties and any_topics:
        # filter by both
        print "not yet"
    elif any_parties:
        # filter by party
        isFirst = True
        count = 0
        votes = "SELECT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_msp AS msp "
        while count < len(parties):
            count += 1
            if isFirst == 1:
                votes = votes + "WHERE (msp.party_id = " + parties[count]
                isFirst = False
            else:
                votes = votes + " OR msp.party_id = " + parties[count]
        votes = votes + ") ORDER BY vote.msp_id"
    elif any_topics:
        #filter by topics
        isFirst = True
        count = -1
        votes = "SELECT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote, msp_division AS div "
        while count < len(topics) - 1:
            count = count + 1
            if isFirst == 1:
                votes = votes + "WHERE (div.topic_id = " + topics[count]
                isFirst = False
            else:
                votes = votes + " OR div.topic_id = " + topics[count]
        votes = votes + ") ORDER BY vote.msp_id"
    else:
        # no filter
        votes = "SELECT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote ORDER BY msp_id"

    cr.execute(votes)
    returned_votes = cr.fetchall()

    return returned_votes