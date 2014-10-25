import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")

from scottviz_app.models import *


def populate_party():
    with open('static/test_data/parties.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            p = add_party(line[1])
            p.save()


def populate_constituency():
    with open('static/test_data/districts.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            c = add_constituency(line[0], line[1], line[2])

def populate_msps():
    i = 0
    with open('../scraper/msp_scraper/msps.csv') as f:
        for line in f:
            line = line.split(';')
            print line
            p = add_party(line[2])
            id = i+1
            fname = line[1]
            lname = line[0]
            c = add_constituency(line[3])
            msp = add_msps(fname, lname, p, id, c)
            msp.save()

def

def add_msps(fname, lname, party, mspid, c):
    return MSP.objects.get_or_create(firstname=fname, lastname=lname, foreignid=mspid, party=party)[0]


def add_party(name):
    return Party.objects.get_or_create(name=name)[0]


def add_constituency(name):
    return Constituency.objects.get_or_create(name=name)[0]


def add_constituency(id, parent, name):
    return Constituency.objects.get_or_create(id=id, parent=parent, name=name)[0]

if __name__ == '__main__':
    populate_constituency()
    populate_party()
    populate_msps()