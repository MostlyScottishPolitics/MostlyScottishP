import mdp
import numpy
import matplotlib.pyplot as plt
import pylab
import fileinput
import os.path
import psycopg2 as pq
import fileinput
import os
import csv

print '' 
print "-----Program Started-----"
print '' 

#Connect to DB
#------Replace with your DB details accordingly--------
cn = pq.connect('dbname=m_14_1006414v user=m_14_1006414v password=1006414v')
cr = cn.cursor()
print "0) Database Connected."

result = cr.execute('SELECT MAX(id) FROM scottviz_app_division;')
maxDivision = cr.fetchone()
result = cr.execute('SELECT COUNT(DISTINCT id) FROM scottviz_app_msp;')
maxMSP = cr.fetchone()

#Convert tuples to list of ints, extract the first (and only value)
maxMSP_int = map(int, maxMSP)[0] + 1
maxDivision_int = map(int, maxDivision)[0] + 1 

#print "max MSP:" + str(maxMSP_int)
#print "max Division:" + str(maxDivision_int)
data = {}
matrix = numpy.zeros((int(maxMSP_int),int(maxDivision_int)))

#Not in use at the moment, self explanatory
def selectMSP():
    cr.execute('SELECT id FROM scottviz_app_msp;')
    count = -1
    mspList=[]
    for row in cr:
        count += 1
        mspList.append(cr.fetchone()[count])
    print "MSP List: " + mspList
    return mspList

#Fills in values of 2D null matrix, with each entry being a vote (X=divisions, Y=MSPs)
def selectVotes():
    #Assumes divisions table will also use foreignid in the same way as MSP
   result = cr.execute("SELECT msp.foreignid, div.id, vote.vote FROM scottviz_app_msp AS msp, scottviz_app_division AS div, scottviz_app_vote AS vote WHERE msp.id = vote.msp_id AND div.id= vote.division_id")
   vote = cr.fetchall()
   count=-1
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
    result = cr.execute("SELECT party.name FROM scottviz_app_party AS party, scottviz_app_msp AS msp WHERE msp.party_id = party.id")
    party = cr.fetchall()
    count = -1
    partyList=[]
    for rows in party:
        count += 1
        party_entry = map(str, party[count])[0]
        partyList.append(party_entry)
    return partyList

matrix = selectVotes()
numpy.savetxt("InputMatrix.csv", matrix, fmt="%s", delimiter=",")
print '2) Input Data stored in matrix, and printed to InputMatrix.csv.'


imdp = mdp.nodes.PCANode(output_dim=2)
output = imdp(matrix)


#Ouput everything to CSV so as to be read by D3
numpy.savetxt("OutputMatrix.csv", output, fmt="%s", delimiter=",")
print "3) PCA Data saved to file."

#Append name of party (as a string) to each row of output text
partyList = selectParty()
count = -1
path = os.path.dirname(os.path.abspath(__file__)) + '\OutputMatrix.csv'
firstLine = 0
for line in fileinput.input('OutputMatrix.csv', inplace=1):
    count += 1
    #If first line of csv add header, else append party name
    if firstLine == 0:
        print 'X, Y, Party'
        firstLine = 1;
    else:
        try:
            print '{0}{1}'.format(line.rstrip('\n'), (',' + partyList[count]))
        except:
           pass

print "4) Parties appended to CSV."
