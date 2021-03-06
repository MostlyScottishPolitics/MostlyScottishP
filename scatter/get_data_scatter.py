__author__ = '2168879m'

import fileinput
import os

import numpy

__author__ = '2168879m'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz import settings
from msp.models import MSP


def get_data_scatter(scores):

    msps = MSP.objects.all()

    data = []
    for msp_id, [x, y] in scores:
        msp_name = msps.get(id=msp_id)
        msp_party = msps.get(id=msp_id).party
        if (numpy.isnan(x)):
            x = '0'
        if (numpy.isnan(y)):
            y = '0'
        data += [[float(x),float(y),str(msp_party),str(msp_name)]]

    return data