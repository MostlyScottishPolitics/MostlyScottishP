import os
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")

from scottviz_app.models import *


def add_msps(fname, lname, party, mspid, fid, c):
    return \
        MSP.objects.get_or_create(firstname=fname, lastname=lname, id=mspid, foreignid=fid, party=party,
                                  constituency=c)[0]


def add_party(name):
    return Party.objects.get_or_create(name=name)[0]


def get_constituency(id):
    return Constituency.objects.get_or_create(id=id)[0]


def add_constituency(id, parent, name):
    return Constituency.objects.get_or_create(id=id, parent=parent, name=name)[0]


def get_msp(id):
    return MSP.objects.get_or_create(id=id)[0]


def get_division(id):
    return Division.objects.get_or_create(id=id)[0]


def add_division(id, parent, date, text, result):
    res = ''
    if result == '1':
        res = models.Division.RESULTS.CARRIED
    elif result == '2':
        pass
    else:
        pass
    if parent != 0:
        return Division.objects.get_or_create(motionid=id, parent=get_division(parent), date=date, motiontext=text, result=res)[0]
    else:
        return Division.objects.get_or_create(motionid=id, parent=None, date=date, motiontext=text, result=res)[0]


def add_vote(msp, div, vote):
    if vote == '0':
        res = models.Vote.YES
    elif vote == '1':
        res = models.Vote.NO
    elif vote == '2':
        res = models.Vote.ABSTAIN
    else:
        res = models.Vote.ABSENT
    return Vote.objects.get_or_create(msp=msp, division=div, vote=res)[0]


def populate_party():
    with open('static/test_data/parties.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            add_party(line[1])


def populate_constituency():
    with open('static/test_data/districts.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            parent = int(float(line[1]))
            name = line[2].strip(" \"\'\r\n")

            if parent == 0:
                add_constituency(id, None, name)
            else:
                add_constituency(id, get_constituency(parent), name)


def populate_msps():
    with open('static/test_data/msps.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            p = add_party(int(float(line[3])))
            id = int(float(line[0]))
            fid = int(float(line[1]))
            fname = line[4]
            lname = line[5]
            constituency_id = int(float(line[2]))
            c = get_constituency(constituency_id)
            add_msps(fname, lname, p, id, fid, c)


def populate_divisions():
    with open('static/test_data/divisions.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            parent = int(float(line[1]))
            identifier = line[2]
            date = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M:%S.%f")
            text = line[5]
            result = line[6]
            add_division(id, parent, date, text, result)


def populate_votes():
    with open('static/test_data/votes.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            print line
            id = int(float(line[0]))
            msp = get_msp(int(float(line[1])))
            division = get_division(int(float(line[2])))
            if line[3] == '0':
                v = "Yes"
            elif line[3] == '1':
                v = "No"
            elif line[3] == '2':
                v = "Abstain"
            else:
                v = "Absent"
            add_vote(id, msp, division, v)


def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()

if __name__ == '__main__':
    delete_data()
    populate_constituency()
    populate_party()
    populate_msps()
   # populate_votes()
   # populate_divisions()
