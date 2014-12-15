import fileinput
import os

import numpy

__author__ = '2168879m'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
outputLocation = settings.STATIC_PATH + '/csv/OutputMatrix.csv'
from msp.models import MSP
from django.db.models import Q

def write_scatter(scores, parties):

    numpy.savetxt(outputLocation, scores, fmt="%s", delimiter=",")
    msps = MSP.objects.all().order_by('id')

    #Filter MSPs to list depending on the parties to display (needed for anything w/ Party Filters)
    #if parties != []:
     #   query = reduce(lambda q,value: q|Q(party=str(value)), parties, Q())
     #   msps = msps.filter(query)

    count = -1
  #  path = os.path.dirname(os.path.abspath(__file__)) + outputLocation
    firstLine = True
    for line in fileinput.input(outputLocation, inplace=1):
        count += 1
        #If first line of csv add header, else append party name
        if firstLine :
            print 'X,Y,Party,MSP Name'
            firstLine = False;
        elif (parties == []) or (str(msps[count].party.id) in parties):
            try:
                print '{0}{1}'.format(line.rstrip('\n'), (',' + str(msps[count].party) + ',' + str(msps[count])))
            except:
                pass
