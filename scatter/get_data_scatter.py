__author__ = '2168879m'

import fileinput
import os

import numpy

__author__ = '2168879m'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
outputLocation = settings.STATIC_PATH + '/csv/OutputMatrix.csv'
from msp.models import MSP


def get_data_scatter(scores):

    msps = MSP.objects.all()

    data = []
    for msp_id, [x, y] in scores:
        msp_name = msps.get(id=msp_id)
        msp_party = msps.get(id=msp_id).party
        data += [[float(x),float(y),str(msp_party),str(msp_name)]]

    print data

    return data