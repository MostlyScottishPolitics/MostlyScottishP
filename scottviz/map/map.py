import fileinput
import os
import psycopg2 as pq
from collections import Counter


#Update me to appropriate output location for CSV to be read by D3
outputLocation = "H:\Spviz-app-master\scottviz\static\csv\OutputMatrix.csv"

print ''
print "-----Program Started-----"
print ''

# Connect to DB
#------Replace with your DB details accordingly--------
cn = pq.connect('dbname=m_14_pgtproja user=m_14_pgtproja password=pgtproja host=yacata.dcs.gla.ac.uk')
cr = cn.cursor()
print "0) Database Connected."

def removeBrackets(stringEntry):
    return str(stringEntry).replace("'",'')


#Gets MSP First and Second Names
def getRegions():
    result = cr.execute('SELECT id FROM scottviz_app_constituency WHERE parent_id IS NULL;')
    region = cr.fetchall()
    count = -1
    regionList = []
    for rows in region:
        count += 1
        regionIds = map(int, region[count])[0]
        regionList.append(regionIds)
    print "Region list " + str(regionList)
    return regionList


def getConstituencies(regionList):
    constituencyRegionList = []
    for s in regionList:
        #regionEntry = removeBrackets(s)
        #print regionEntry
        result = cr.execute('SELECT id FROM scottviz_app_constituency WHERE parent_id = %s', (s,))
        constituency = cr.fetchall()
        count = -1
        constituencyList = []
        for rows in constituency:
            count += 1
            constituencyIds = map(int, constituency[count])[0]
            constituencyList.append(constituencyIds)
        print "Constituency list " + str(constituencyList)
        constituencyRegionList.append(constituencyList)
    return constituencyRegionList

def partyCountPerConstituency(constituencyRegionList, regionList):
    print regionList
    regionCount = 0
    constituencyList = []
    for s in constituencyRegionList:
        constituencyList = []
        print 'Region: ' + str(regionList[regionCount])
        regionCount = regionCount + 1
        for t in s:
            result = cr.execute('SELECT party_id, constituency_id FROM scottviz_app_msp WHERE constituency_id = %s', (t,))
            party = cr.fetchall()
            count = -1
            partyList = []
            for rows in party:
                count += 1
                partyIds = map(int, party[count])[0]
                constituencyIds = map(int, party[count])[1]
                partyList.append(partyIds)
                print "Party with ID " + str(partyList) + " manages Constituency with ID " + str(constituencyIds)
        counter = Counter(partyList)

    return partyList

regionList = getRegions()
constituencyRegionList = getConstituencies(regionList)
partyCountPerConstituency(constituencyRegionList, regionList)
