import fileinput
import os

import numpy
import psycopg2 as pq

import mdp

#Update me to appropriate output location for CSV to be read by D3
outputLocation = "H:\Spviz-app\Spviz-app\scottviz\static\csv\OutputMatrix.csv"

print ''
print "-----Program Started-----"
print ''

# Connect to DB
#------Replace with your DB details accordingly--------
cn = pq.connect('dbname=m_14_pgtproja user=m_14_pgtproja password=pgtproja host=yacata.dcs.gla.ac.uk')
cr = cn.cursor()
print "0) Database Connected."

result = cr.execute('SELECT MAX(id) FROM msp_division;')
maxDivision = cr.fetchone()
result = cr.execute('SELECT COUNT(DISTINCT id) FROM msp_msp;')
maxMSP = cr.fetchone()

#Convert tuples to list of ints, extract the first (and only value)
maxMSP_int = map(int, maxMSP)[0] + 1
maxDivision_int = map(int, maxDivision)[0] + 1

#print "max MSP:" + str(maxMSP_int)
#print "max Division:" + str(maxDivision_int)
data = {}
matrix = numpy.zeros((int(maxMSP_int), int(maxDivision_int)))

#Gets MSP First and Second Names
def selectMSP():
    result = cr.execute('SELECT firstname, lastname FROM msp_msp ORDER BY foreignid;')
    msp = cr.fetchall()
    count = -1
    mspList = []
    for rows in msp:
        count += 1
        msp_entry = map(str, msp[count])[0]
        msp_entry = msp_entry + ' ' + map(str, msp[count])[1]
        mspList.append(msp_entry)
    #print "MSP List: " + mspList
    return mspList


#Fills in values of 2D null matrix, with each entry being a vote (X=divisions, Y=MSPs)
def selectVotes():
    result = cr.execute(
        "SELECT msp.foreignid, div.id, vote.vote FROM msp_msp AS msp, msp_division AS div, msp_vote AS vote WHERE msp.id = vote.msp_id AND div.id= vote.division_id ORDER BY msp.foreignid")
    vote = cr.fetchall()
    count = -1
    for rows in vote:
        count += 1
        msp_entry = map(int, vote[count])[0]
        division_entry = map(int, vote[count])[1]
        vote_entry = map(int, vote[count])[2]
        try:
            matrix[msp_entry][division_entry] = vote_entry
        except:
            print "ERROR!!"
            print "MSP Entry: " + msp_entry
            print "Division Entry: " + division_entry
    print "1) Data has been retrieved from database."
    return matrix

#Gets each MSP's Party's name
def selectParty():
    result = cr.execute(
        "SELECT party.name FROM msp_party AS party, msp_msp AS msp WHERE msp.party_id = party.id ORDER BY msp.foreignid")
    party = cr.fetchall()
    count = -1
    partyList = []
    for rows in party:
        count += 1
        party_entry = map(str, party[count])[0]
        partyList.append(party_entry)
    return partyList


matrix = selectVotes()
#Slightly hacky solution to removing null first row and column which exist as a bi-product of required matrix dimensions
matrix = numpy.delete(matrix,(0),axis=0)
matrix = numpy.delete(matrix,(0),axis=1)

numpy.savetxt("InputMatrix.csv", matrix, fmt="%s", delimiter=",")
print '2) Input Data stored in matrix, and printed to InputMatrix.csv.'

imdp = mdp.nodes.PCANode(output_dim=2)
output = imdp(matrix)


#Ouput everything to CSV so as to be read by D3
numpy.savetxt(outputLocation, output, fmt="%s", delimiter=",")
print "3) PCA Data saved to file."

#Append name of party (as a string) to each row of output text
mspList = selectMSP()
partyList = selectParty()
count = -1
path = os.path.dirname(os.path.abspath(__file__)) + outputLocation
firstLine = 0
for line in fileinput.input(outputLocation, inplace=1):
    count += 1
    #If first line of csv add header, else append party name
    if firstLine == 0:
        print 'X,Y,Party,MSP Name'
        firstLine = 1;
    else:
        try:
            print '{0}{1}'.format(line.rstrip('\n'), (',' + partyList[count] + ',' + mspList[count]))
        except:
            pass

print "4) Parties appended to CSV."
