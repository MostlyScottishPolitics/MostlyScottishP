__author__ = '2168879m'

# run to repopulate divisions and vote
# should probably be followed up by updating the db with the computable statistics

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spviz.scottviz.scottviz.settings")
from Spviz.scottviz.scottviz_app.models import *
from data import *
from dateutil import parser
from xml.dom import minidom
from string import replace, upper


def get_files(d):
    return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]

def absent_votes(division):
    # if an msp did not have a vote read, he/she was absent

    # get votes read until now
    votes_read = Vote.objects.filter(division=division)
    # get msps that didn't vote
    absentMSPs = MSP.objects.all()
    for vote in votes_read:
        absentMSPs = absentMSPs.exclude(foreignid=vote.msp.foreignid)
    # those msps had an absent vote
    for msp in absentMSPs:
        v = Vote(msp=msp, division=division, vote=Vote.ABSENT)
        v.save()

def get_votes(parsing_law,division,type):
    if len(parsing_law.getElementsByTagName(type)):
        msps = parsing_law.getElementsByTagName(type)[0].getElementsByTagName("msp")
        for msp in msps:
            firstname = msp.getElementsByTagName("name")[0].firstChild
            lastname = msp.getElementsByTagName("surname")[0].firstChild
            if firstname and lastname:
                firstname = str(firstname.data)
                lastname = str(lastname.data)
                # check for recorded errors with scraper
                if lastname == 'Mackenzie':
                    lastname =  'MacKenzie'
                if lastname == 'GIBson':
                    lastname =  'Gibson'
                if lastname != 'Copy':
                    msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                    v = Vote(msp=msp, division=division, vote=Vote.YES)
                    v.save()

def populate_divisions_from(files_location,startdate,enddate):

    # naive skip files before startdate and after enddate, using a switch: currentsession

    currentsession = False

    files = get_files(files_location)

    for f in files:

        # get date
        doc = minidom.parse(f)
        date = doc.getElementsByTagName("date")[0].firstChild.data
        dt = parser.parse(date).date()

        # startdate reached
        if date == startdate:
            currentsession = True

        # enddate reached
        if date == enddate:
            currentsession = False

        if currentsession:
            laws = doc.getElementsByTagName("law")
            # parse each law
            for law in laws:

                motiontype = law.getElementsByTagName("type")
                if motiontype != []:
                    if motiontype[0].FirsChild.data == "motion":
                        motion = True

                motionid = law.getElementsByTagName("id")[0].firstChild.data

                motiontopic = law.getElementsByTagName("topic")[0].firstChild.data.encode('latin1','backslashreplace').replace("\\u2019","\'")

                text_raw = law.getElementsByTagName("text")
                if text_raw == [] :
                    text='n/a'
                else:
                    text = text_raw[0].firstChild.data.encode('latin1','backslashreplace').replace("\\u2019","\'")

                topic_raw = law.getElementsByTagName("category")
                if topic_raw == [] :
                    topic='Unknown'
                else:
                    topic = topic_raw[0].firstChild.data.encode('latin1','backslashreplace').replace("\\u2019","\'")

                # parsed most info for division
                division = Division(parent=None, motion=motion, motionid=motionid, motiontext=text.decode('latin1'), motiontopic=motiontopic.decode('latin1'), topic=topic.decode('latin1'), date=dt)

                # get result for this division
                yup = law.getElementsByTagName("agreed")[0].firstChild
                if yup:
                    if yup.data == "agreed":
                        division.result = 1
                    else:
                        division.result = 2
                # done with division
                division.save()

                # read the votes
                get_votes(law, division, "for")
                get_votes(law, division, "against")
                get_votes(law, division, "abstention")
                absent_votes(division)


if __name__ == '__main__':
    Division.objects.all().delete()
    Vote.objects.all().delete()
    print "_deleted_old_divisions_and_votes_"
    populate_divisions_from(divisions_location, startdate, enddate)
    print "_read_new_divisions_and_votes_"