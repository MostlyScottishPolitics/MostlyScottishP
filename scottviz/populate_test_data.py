import os
from scottviz.settings import STATIC_PATH

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from scottviz_app.models import *


def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()


def populate_party():
    with open(STATIC_PATH+'/test_data/parties.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            p = Party.objects.get_or_create(name=line[1], id=int(float(line[0])))[0]
            p.save()


def populate_constituency():
    with open(STATIC_PATH+'/test_data/districts.csv') as f:
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
    with open(STATIC_PATH+'/test_data/msps.csv') as f:
        next(f)
        for row in f:
            row = row.split(',')
            p = Party.objects.get(id=int(float(row[3])))
            fid = int(float(row[1]))
            c = Constituency.objects.get(id=int(float(row[2])))
            m = MSP(id=int(float(row[0])),firstname=row[4], lastname=row[5], constituency=c, party=p, foreignid=fid)
            m.save()


def populate_votes():
    with open(STATIC_PATH+'/test_data/votes.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            print line
            id = int(float(line[0]))
            msp = MSP.objects.get(id=int(float(line[1])))
            division = Division.objects.get(id=int(float(line[2])))
            if line[3] == '0':
                v = models.Vote.ABSENT
            elif line[3] == '1':
                v = models.Vote.ABSTAIN
            elif line[3] == '2':
                v = models.Vote.YES
            elif line[3] == '3':
                v = models.Vote.NO
            vote = Vote(id=id, msp=msp, division=division, votes=v)
            vote.save()


def populate_divisions():
    with open(STATIC_PATH+'/test_data/divisions.csv') as f:
        next(f)
        for row in f:
            row = row.split(',')
            id = int(float(row[0]))
            parent = int(float(row[1]))
            print parent
            identifier = row[2]
            text = row[5]
            result = row[6]
            if row[6] == '0':
                result = models.Division.CARRIED
            elif row[6] == '1':
                result = models.Division.DEFEATED
            else:
                pass

            if parent == 0:
                d = Division(id=id, parent=None, motiontext=text, motionid=identifier, result=result)
                d.save()
            else:
                pere = Division.objects.get(id=parent)
                d = Division(id=id, parent=pere, motiontext=text, motionid=identifier, result=result)
                d.save()


if __name__ == '__main__':
    delete_data()
    populate_party()
    populate_constituency()
    populate_msps()
    populate_divisions()
    populate_votes()
