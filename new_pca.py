import mdp
import numpy
import matplotlib.pyplot as plt
import pylab
import os.path
import psycopg2 as pq
import fileinput

#Connect to DB
#------Replace with your DB details accordingly--------
cn = pq.connect('dbname=m_14_1006414v user=m_14_1006414v password=1006414v')
cr = cn.cursor()
maxDivision = cr.execute('SELECT MAX(foreignid) FROM scottviz_app_division;')
maxMSP = cr.execute('SELECT MAX(foreignid) FROM scottviz_app_msps;')
data = {}
matrix = numpy.zeros((maxDivisions, maxMSP))

#Not in use at the moment, self explanatory
def selectMSP():
    cr.execute('SELECT id FROM scottviz_app_msp;')
    count = 0
    mspList=[]
    for row in cr:
        ++count
        mspList.append(cr.fetchone()[count])
    print "MSP List: " + mspList
    return mspList

#Fills in values of 2D null matrix, with each entry being a vote (X=divisions, Y=MSPs)
def selectVotes():
    #Assumes divisions table will also use foreignid in the same way as MSP
   vote = cur.execute("SELECT msp.foreignid, div.foreignid, vote.vote FROM scottviz_app_msp AS msp, scottviz_app_division AS div, votescottviz_app_vote AS vote WHERE msp.id = vote.msp_id AND div.foreignid = vote.division_id")
   for rows in vote:
       matrix[vote['msp.foreignid']][vote['div.foreignid']] = vote['vote.vote']
   return matrix

#Gets each MSP's Party's name
def selectParty():
    party = cur.execute("SELECT party.name FROM scottviz_app_party AS party, scottviz_app_msp AS msp WHERE msp.party_id = party.id")
    count = 0
    partyList=[]
    for row in party:
        ++count
        partyList.append(cr.fetchone()[count])

matrix = selectVotes()
print 'Data to be PCAed'
print matrix

#Specify 2D PCA output, PCA, and print results to screen
imdp = mdp.nodes.PCANode(output_dim=2)
ouptut = imdp(matrix)
print 'PCA Output'
print output

#Ouput everything to CSV so as to be read by D3
print "Data saved to file"
numpy.savetxt("OuputMatrix.csv", output, fmt="%s", delimiter=",")

#Append name of party (as a string) to each row of output text
partyList = selectParty()
count = 0
for line in fileinput.input('OutputMatrix.csv', inplace=1):
    ++count
    print '{0}{1}'.format(line.rstrip('\n'), (', ' + partyList[count]))

#Uncomment to visualize using python
#cm = plt.cm.get_cmap('RdYlBu')
#z = output
#fig = plt.figure()
#ax = fig.add_subplot(111)

#ax.scatter(output[:,0], output[:,1], c='r', marker='o')
#plt.show()
