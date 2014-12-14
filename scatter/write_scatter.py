import fileinput
import os

import numpy

__author__ = '2168879m'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
outputLocation = settings.STATIC_PATH + '/csv/OutputMatrix.csv'
from msp.models import MSP

def write_scatter(scores, parties):

    numpy.savetxt(outputLocation, scores, fmt="%s", delimiter=",")
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