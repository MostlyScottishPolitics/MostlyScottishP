import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
import xml.etree.ElementTree as ET
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
            m = MSP(firstname=row[1], lastname=row[0], constituency=c, party=p, foreignid=i)
            m.save()


def populate_votes(files):
    for file in files:
        doc = minidom.parse(file)
        date = doc.getElementsByTagName("date")[0]
        print date



def read_data():
    """

    :rtype : object
    """
    tree = ET.parse('../scraper/report_scraper/data_30_09_2014.xml')
    root = tree.getroot()
    for child in root:
      print child.tag, child.attrib


# Might be useful to change such that we get the files only for a specific interval, based on begin-end dates
# this change can be of use for different sessions of parliament or simply for updating?
# For now, I can check for dates for this session while parsing the sml files. But it would be much more efficient to do it here
def get_files(d):
        return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d,f))]

if __name__ == '__main__':
    delete_data()
    populate_constituency()
    populate_msps()
    populate_votes(get_files('../scraper/report_scraper/data/'))
    read_data()