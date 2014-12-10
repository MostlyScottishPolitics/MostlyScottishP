from Spviz.scottviz.msp.models import *

__author__ = '2168879m'

# run to get default db

import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.msp.settings")
from data import *
from dateutil import parser
from populate_divisions import populate_divisions_from



def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()
    Job.objects.all().delete()


def populate_constituency():
    with open('../scottviz/static/test_data/districts.csv') as f:
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


def populate_current_msps():
    with open('../scraper/msp_scraper/msps.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            row = row[0].split(';')
            p = Party.objects.get_or_create(name=row[2].strip())[0]
            p.save()
            c = Constituency.objects.get(name=row[3].strip())
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i, status=MSP.MEMBER,         # basic data, sufficient to run visualisations & website
                    member_startdate = parser.parse('5 May 2011').date(), member_enddate = parser.parse('5 May 2016').date(),   # (as they should allow nulls for other fields)
                    party_startdate = parser.parse('5 May 2011').date(), party_enddate = parser.parse('5 May 2016').date())     # default ranges, will be overwritten for the few msps that move about
            m.save()


# get msps that were not in the parliment at the time of scraping
def populate_former_msps():
    for (constituency,party,msp) in former_or_new_msps:
        m = msp
        m.constituency = Constituency.objects.get(name = constituency)
        m.party = Party.objects.get(name = party)
        m.save()

# update dates for new msps
def update_new_msps():
    m = MSP.objects.get(lastname='Allard',firstname ='Christian')
    m.member_startdate = parser.parse('15 May 2013')
    m.save()
    m = MSP.objects.get(lastname='Buchanan',firstname ='Cameron')
    m.member_startdate = parser.parse('4 September 2013')
    m.save()

# photos for all msps in the db
def msp_photos():
    msps = MSP.objects.all()
    for msp in msps:
        name = str(msp)
        if name in msp_img_urls.keys():
            msp.img = msp_img_urls[name]
            msp.save()

# jobs for all msps in db
def msp_jobs():
    i=0
    for job in jobs:
        i+=1
        j = Job(job_foreignid=i,name=job[2],msp=MSP.objects.get(firstname=job[0], lastname=job[1]),job_startdate=job[3],job_enddate=job[4])
        j.save()

if __name__ == '__main__':
    delete_data()
    populate_constituency()
    print "_constituency_"
    populate_current_msps()
    print "_current_msps_and_parties"
    populate_former_msps()
    print "_former_msps_"
    update_new_msps()
    print "_new_msps_"
    msp_photos()
    print "_photos_for_all_msps_"
    msp_jobs()
    print "_all_jobs_"
    # reads new scraped data; can be run to overwrite from populate_divisions
    populate_divisions_from(divisions_location, startdate, enddate)
    print "_read_divisions_and_votes_"
    # updates analytics; can be run to overwrite only for some from uptadedb
    os.system('updatedb.py')
    print "_analytics_done_"
    print "_done_"
