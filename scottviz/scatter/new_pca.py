import csv

__author__ = '2165430C'
import fileinput
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
from msp.models import MSP, Division, Party, Vote
import numpy
import psycopg2 as pq
import mdp

outputLocation = settings.STATIC_PATH + '/csv/OutputMatrix.csv'

# README:
#No arguments will run the script without any filters
#If the first argument is 1, the script will treat every subsequent argument as a party filter (as per each party's id in the DB)
#Do not forget to edit the variable 'outputLocation' as necessary
#Do not forget to update DB details as necessary


def createQuery(cr, query, filter, parties, topics):
    output = ""

    if query == "votes":
        #No Filter
        if filter == 0:
            output = "SELECT vote.msp_id, vote.division_id, vote.vote FROM msp_vote AS vote ORDER BY msp_id"
           # output = Vote.objects.all()

            return output
        #Party Filter
        elif filter == 1:
            isFirst = 1
            count = 0
            output = "SELECT msp.foreignid, div.id, vote.vote FROM msp_msp AS msp, msp_division AS div," \
                     " msp_vote AS vote WHERE msp.id = vote.msp_id AND div.id= vote.division_id "
            while count < len(parties):
                count += 1
                getDistinctParties(cr, parties[count])
                if isFirst == 1:
                    output = output + "AND (msp.party_id = " + parties[count]
                    isFirst = 0
                else:
                    output = output + " OR msp.party_id = " + parties[count]
            output = output + ") ORDER BY msp.foreignid"
        #Topic Filter
        elif filter == 2:
            isFirst = 1
            count = -1
            output = "SELECT msp.foreignid, div.id, vote.vote FROM msp_msp AS msp, msp_division AS div," \
                     " msp_vote AS vote WHERE msp.id = vote.msp_id AND div.id= vote.division_id "
            while count < len(topics) - 1:
                count = count + 1
                if isFirst == 1:
                    output = output + "AND (div.topic_id = " + topics[count]
                    isFirst = 0
                else:
                    output = output + " OR div.topic_id = " + topics[count]
            output = output + ") ORDER BY msp.foreignid"
    return output


def getDistinctParties(cr, nameFromQuery):
    #Check if ID is a suitable value
    id = cr.execute('SELECT name FROM msp_party WHERE id= %s',
                    (nameFromQuery,))  #[party.name for party in Party.objects.filter(id=nameFromQuery)](0)

    try:
        idOutput = map(str, id)[0]
    except:
        print "Couldn't find PartyID: " + nameFromQuery + " in database - Are you sure you're passing the right value?"

    return nameFromQuery


def handleArguments(parties, topics):
    global filter

    if parties:
        filter = 1
    if topics:
        filter = 2
    else:
        filter = 0


#Fills in values of 2D null matrix, with each entry being a vote (X=divisions, Y=MSPs)
def selectVotes(cr, matrix, parties, topics):
    result = cr.execute(createQuery(cr, "votes", filter, parties, topics))
    votes = cr.fetchall()
    count = -1

    shift_msps = int(votes[0][0])

    shift_division = int(votes[0][1])

    for vote in votes:
        msp_entry = int(vote[0])
        division_entry = int(vote[1])
        vote_entry = int(vote[2])
        try:
            matrix[msp_entry-shift_msps][division_entry-shift_division] = vote_entry
        except:
            print "ERROR!!"
            print "MSP Entry: " + str(msp_entry)
            print "Division Entry: " + str(division_entry)
    return matrix


# not in use
def get_matrix(matrix):
    votes = Vote.objects.all()
    for vote in votes:
        matrix[vote.msp.foreignid-1][vote.division.id-1] = vote.vote
    print "at least this is done"
    return matrix


def new_pca(parties, topics):
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

    handleArguments(parties, topics)

    maxMSP_int = MSP.objects.count()
    maxDivision_int = Division.objects.count()


    #Create null matrix (to be replaced with value wherever an msp voted on a division)
    matrix = numpy.zeros(shape=(maxMSP_int, maxDivision_int))

    matrix = selectVotes(cr, matrix, parties, topics)
   # matrix = get_matrix(matrix)

    #Deletes every all-zero row in the input matrix (this is necessary for the filters to work correctly)
    matrix = matrix[~numpy.all(matrix == 0, axis=1)]

    numpy.savetxt(settings.STATIC_PATH + "/csv/InputMatrix.csv", matrix, fmt="%s", delimiter=",")


    #PCA magic happens here using MDP
    imdp = mdp.nodes.PCANode(output_dim=2)
    output = imdp(matrix)

    #Ouput everything to CSV so as to be read by D3/Javascript
    numpy.savetxt(outputLocation, output, fmt="%s", delimiter=",")


    #Append name of party and MSP names(as a string) to each row of output text
    msps = MSP.objects.all().order_by('id')
    count = -1
    path = os.path.dirname(os.path.abspath(__file__)) + outputLocation
    firstLine = 0
    for line in fileinput.input(outputLocation, inplace=1):
        count += 1
        #If first line of csv add header, else append party name
        if firstLine == 0:
            print 'X,Y,Party,MSP Name'
            firstLine = 1;
        elif (parties == []) or (str(msps[count].party.id) in parties):
            try:
                print '{0}{1}'.format(line.rstrip('\n'), (',' + str(msps[count].party) + ',' + str(msps[count])))
            except:
                pass

    print "done!"




