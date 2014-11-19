import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from dateutil import parser
from xml.dom import minidom
from scottviz_app.models import *


def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()


def populate_constituency():
    with open('static/test_data/districts.csv') as f:
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
    with open('../scraper/msp_scraper/msps.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            row = row[0].split(';')
            p = Party.objects.get_or_create(name=row[2].strip())[0]
            p.save()
            c = Constituency.objects.get(name=row[3].strip())
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i)
            m.save()


def populate_votes(files):
    # naive skip files before 06 May 2011, using a switch: currentsession
    # change encouraged
    currentsession = False
    for f in files:
        doc = minidom.parse(f)
        date = doc.getElementsByTagName("date")[0].firstChild.data
        dt = parser.parse(date).date()

        if date == '09 June 2011':
            currentsession = True

        if currentsession:
            laws = doc.getElementsByTagName("law")

            for law in laws:
                motionid = law.getElementsByTagName("id")[0].firstChild.data
                yup = law.getElementsByTagName("agreed")[0].firstChild

                if yup:
                    if yup.data == "agreed":
                        d = Division(parent=None, motionid=motionid, result=1, date=dt)
                        d.save()
                    else:
                        d = Division(parent=None, motionid=motionid, result=2, date=dt)
                        d.save()
                else:
                    # TO DO: see if agreeed or disagreed from votes
                    d = Division(parent=None, motionid=motionid, date=dt)
                    d.save()

                if len(law.getElementsByTagName("for")):
                    forMSPs = law.getElementsByTagName("for")[0].getElementsByTagName("msp")
                    for msp in forMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname not in ['Allan', 'Simpson', 'Mackenzie', 'Copy', 'GIBson']:
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.YES)
                                v.save()

                if len(law.getElementsByTagName("against")):
                    againstMSPs = law.getElementsByTagName("against")[0].getElementsByTagName("msp")
                    for msp in againstMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname not in ['Allan', 'Simpson', 'Mackenzie', 'Copy', 'GIBson']:
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.NO)
                                v.save()

                if len(law.getElementsByTagName("abstain")):
                    abstainMSPs = law.getElementsByTagName("abstain")[0].getElementsByTagName("msp")
                    for msp in abstainMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname not in ['Allan', 'Simpson', 'Mackenzie', 'Copy', 'GIBson']:
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.ABSTAIN)
                                v.save()


def add_other_msps():
    m = MSP(firstname='Brian', lastname='Adam', constituency=Constituency.objects.get(name='Aberdeen Donside'),
            party=Party.objects.get(name='Scottish National Party'), foreignid=129)
    m.save()
    m = MSP(firstname='Helen', lastname='Eadie', constituency=Constituency.objects.get(name='Cowdenbeath'),
            party=Party.objects.get(name='Scottish Labour'), foreignid=130)
    m.save()
    m = MSP(firstname='Margo', lastname='MacDonald', constituency=Constituency.objects.get(name='Lothian'),
            party=Party.objects.get(name='Independent'), foreignid=131)
    m.save()
    m = MSP(firstname='David', lastname='McLetchie', constituency=Constituency.objects.get(name='Lothian'),
            party=Party.objects.get(name='Scottish Conservative and Unionist Party'), foreignid=132)
    m.save()
    m = MSP(firstname='John', lastname='Park', constituency=Constituency.objects.get(name='Mid Scotland and Fife'),
            party=Party.objects.get(name='Scottish Labour'), foreignid=133)
    m.save()
    m = MSP(firstname='Bill', lastname='Walker', constituency=Constituency.objects.get(name='Dunfermline'),
            party=Party.objects.get(name='Independent'), foreignid=134)
    m.save()


# Might be useful to change such that we get the files only for a specific interval, based on begin-end dates
# this change can be of use for different sessions of parliament or simply for updating?
# For now, I can check for dates for this session while parsing the sml files. But it would be much more efficient to do it here
def get_files(d):
    return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]


if __name__ == '__main__':
    delete_data()
    populate_constituency()
    print "_const_"
    populate_msps()
    print "_msps_"
    add_other_msps()
    print "_other_"
    populate_votes(get_files('../scraper/report_scraper/data/'))
    print "_done_"
