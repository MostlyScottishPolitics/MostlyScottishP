__author__ = '2168879m'

# run to repopulate divisions and vote
# should probably be followed up by updating the db with the computable statistics

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spviz.scottviz.scottviz.settings")
from Spviz.scottviz.scottviz_app.models import *
from data import *
from dateutil import parser
from xml.dom import minidom


def get_files(d):
    return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]


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

            for law in laws:

                motionid = law.getElementsByTagName("id")[0].firstChild.data

                motiontopic_raw = law.getElementsByTagName("topic")[0].firstChild.data
                motiontopic = motiontopic_raw.encode('ascii','replace')

                text_raw = law.getElementsByTagName("text")
                if text_raw == [] :
                    text='n/a'
                else:
                    text_less_raw = text_raw[0].firstChild.data
                    text = str(text_less_raw.encode('ascii','replace'))
                yup = law.getElementsByTagName("agreed")[0].firstChild

                topic = ""

                if yup:
                    if yup.data == "agreed":
                        d = Division(parent=None, motionid=motionid, motiontext=text, motiontopic=motiontopic, topic = topic, result=1, date=dt)
                        d.save()
                    else:
                        d = Division(parent=None, motionid=motionid, motiontext=text, motiontopic=motiontopic,topic = topic, result=2, date=dt)
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
                            if lastname == 'Mackenzie':
                                lastname =  'MacKenzie'
                            if lastname == 'GIBson':
                                lastname =  'Gibson'
                            if lastname != 'Copy':
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
                            if lastname == 'Mackenzie':
                                lastname =  'MacKenzie'
                            if lastname == 'GIBson':
                                lastname =  'Gibson'
                            if lastname !='Copy':
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.NO)
                                v.save()

                if len(law.getElementsByTagName("abstention")):
                    abstainMSPs = law.getElementsByTagName("abstention")[0].getElementsByTagName("msp")
                    for msp in abstainMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname == 'Mackenzie':
                                lastname =  'MacKenzie'
                            if lastname == 'GIBson':
                                lastname =  'Gibson'
                            if lastname !='Copy':
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.ABSTAIN)
                                v.save()

                votes_divison = Vote.objects.filter(division=d)
                allMSPs = set(MSP.objects.all())
                for vote in votes_divison:
                    absentMSPs = [msp for msp in allMSPs if msp!= vote.msp]
                for msp in absentMSPs:
                    v = Vote(msp = msp, division = d, vote = Vote.ABSENT)
                    v.save()


if __name__ == '__main__':
    Division.objects.all().delete()
    print "_deleted_old_divisions_"
    populate_divisions_from(divisions_location, startdate, enddate)
    print "_new_divisions_and_votes_"