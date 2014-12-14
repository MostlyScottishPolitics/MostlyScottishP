"""
Not in use
"""

import csv
import os
import datetime

from msp.models import *
from scottviz.settings import STATIC_PATH


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")


def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()


def populate_party():
    with open(STATIC_PATH + '/test_data/parties.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            p = Party.objects.get_or_create(name=line[1], id=int(float(line[0])))[0]
            p.save()


def populate_constituency():
    with open(STATIC_PATH + '/test_data/districts.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            parent = int(float(line[1]))
            name = line[2].strip(" \"\'\r\n")

            if parent == 0:
                c = Constituency(id=id, parent=None, name=name)
                c.save()

            else:
                pere = Constituency.objects.get(id=parent)
                c = Constituency(id=id, parent=pere, name=name)
                c.save()


def populate_msps():
    with open(STATIC_PATH + '/test_data/msps.csv') as f:
        next(f)
        for row in f:
            row = row.split(',')
            p = Party.objects.get(id=int(float(row[3])))
            fid = int(float(row[1]))
            c = Constituency.objects.get(id=int(float(row[2])))
            m = MSP(id=int(float(row[0])), firstname=row[4], lastname=row[5], constituency=c, party=p, foreignid=fid,
                    img=row[len(row) - 1].strip())
            m.save()


def populate_votes():
    with open(STATIC_PATH + '/test_data/votes.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            msp = MSP.objects.get(id=int(float(line[1])))
            division = Division.objects.get(id=int(float(line[2])))
            v = None
            if line[3] == '0':
                v = models.Vote.ABSENT
            elif line[3] == '1':
                v = models.Vote.ABSTAIN
            elif line[3] == '2':
                v = models.Vote.YES
            elif line[3] == '3':
                v = models.Vote.NO
            vote = Vote.objects.get_or_create(id=id, msp=msp, division=division, vote=v)[0]
            print vote.msp
            vote.save()


def populate_divisions():
    f = open(STATIC_PATH + '/test_data/divisions.csv')
    csv_f = csv.reader(f)
    next(csv_f)
    for row in csv_f:
        id = int(float(row[0]))
        parent = int(float(row[1]))
        identifier = row[2].strip()
        text = row[5]
        result = row[len(row) - 2]
        if len(identifier) > 12:
            identifier = 'missing'
        if row[len(row) - 2] == '1':
            result = Division.DEFEATED
        elif row[len(row) - 2] == '2':
            result = Division.CARRIED
        if parent == 0:
            d = Division(id=id, parent=None, date=datetime.date.today(), motionid=identifier, result=result)
            d.save()
        else:
            pere = Division.objects.get(id=parent)
            d = Division(id=id, parent=pere, motiontext=text, date=datetime.date.today(), motionid=identifier,
                         result=result)
            d.save()


if __name__ == '__main__':
    delete_data()
    populate_party()
    populate_constituency()
    populate_msps()
    populate_divisions()
    populate_votes()
