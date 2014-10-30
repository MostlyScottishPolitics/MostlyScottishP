import json
import requests

import re
from models import Constituency, MSP

__author__ = 'laura'


def is_valid(postcode):
    postcode = postcode.upper()
    postcode = re.sub('\s+', '', postcode)
    inward = 'ABDEFGHJLNPQRSTUWXYZ'
    fst = 'ABCDEFGHIJKLMNOPRSTUWYZ'
    sec = 'ABCDEFGHJKLMNOPQRSTUVWXY'
    thd = 'ABCDEFGHJKSTUW'
    fth = 'ABEHMNPRVWXY'

    return None != (re.match('[%s][1-9]\d[%s][%s]$' % (fst, inward, inward), postcode) or
                    re.match('[%s][1-9]\d\d[%s][%s]$' % (fst, inward, inward), postcode) or
                    re.match('[%s][%s]\d\d[%s][%s]$' % (fst, sec, inward, inward), postcode) or
                    re.match('[%s][%s][1-9]\d\d[%s][%s]$' % (fst, sec, inward, inward), postcode) or
                    re.match('[%s][1-9][%s]\d[%s][%s]$' % (fst, thd, inward, inward), postcode) or
                    re.match('[%s][%s][1-9][%s]\d[%s][%s]$' % (fst, sec, fth, inward, inward), postcode))


def get_constituencies(postcode):
    if not is_valid(postcode):
        return {'ERROR': "Invalid postcode."}

    r = requests.get("http://mapit.mysociety.org/postcode/" + postcode)
    if r.status_code != 200:
        return {'ERROR': "There was an error looking up that postcode."}

    data = json.loads(r.content)
    areas = data['areas']
    regions = {}
    for item in areas:
        if areas[item]['type_name'].startswith("Scottish Parliament constituency"):
            regions['constituency'] = [str(areas[item]['name'])]
        if areas[item]['type_name'].startswith("Scottish Parliament region"):
            regions['region'] = [str(areas[item]['name'])]

    return regions


def get_msps(postcode):
    regions = get_constituencies(postcode)
    if regions['ERROR'] is not None:
        return regions

    print regions
    msps = {}
    for item in regions:
        print regions[item][0]
        const = Constituency.objects.filter(name=regions[item][0])
        for c in const:
            msps[regions[item][0]] = MSP.objects.filter(constituency=c.id)
    return msps, regions


