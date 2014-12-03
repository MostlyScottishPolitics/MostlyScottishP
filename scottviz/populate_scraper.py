import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from dateutil import parser
from decimal import *
from xml.dom import minidom
from scottviz_app.models import *

# images from http://www.scottish.parliament.uk/msps/53234.aspx, need to include licence
# TO DO: more manual urls??  or photos from Pierre
msp_img_urls = {
'George Adam' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853219542.jpg",
'Jackie Baillie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853239417.jpg",
'Richard Baker' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853241871.jpg",
'Claudia Beamish' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853242760.jpg",
'Chic Brodie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853248470.jpg",
'Gavin Brown' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853249293.jpg",
'Keith Brown' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853250168.jpg",
'Margaret Burgess' : "http://www.scottish.parliament.uk/images/MSP%20Photos/BurgessMargaretIG.jpg",
'Malcom Chisholm' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853233410.jpg",
'Angela Constance' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853259652.jpg",
'Bruce Crawford' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853260503.jpg",
'Graeme Dey' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853220957.jpg",
'Nigel Don' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853221226.jpg",
'Bob Doris' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853222113.jpg",
'Kezia Dugdale' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853226958.jpg",
'Jim Eadie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853227726.jpg",
'Annabelle Ewing' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853231910.jpg",
'Fergus Ewing' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853232448.jpg",
'Linda Fabiani' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853240611.jpg",
'Mary Fee' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853240870.jpg",
'Patricia Ferguson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853242528.jpg",
'Neil Findlay' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853244349.jpg",
'John Finnie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853245791.jpg",
'Joe Fitzpatrick' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853249335.jpg",
'Murdo Fraser' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853250520.jpg",
'Rob Gibson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853255175.jpg",
'Annabel Goldie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853257110.jpg",
'Rhoda Grant' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853216633.jpg",
'Iain Gray' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853225741.jpg",
'Mark Griffin' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853262248.jpg",
'Patrick Harvie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853480137.jpg",
'Hugh Henrie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853480588.jpg",
'Jamie Hepburn' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853481923.jpg",
'Fiona Hyslop' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853484194.jpg",
'Adam Ingram' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853485554.jpg",
'Colin Keir' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853499797.jpg",
'Johann Lamont' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853504141.jpg",
'John Lamont' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853504882.jpg",
'Richard Lochhead' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853506741.jpg",
'Kenny MacAskill' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853507149.jpg",
'Angus MacDonald' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853507900.jpg",
'Gordon MacDonald' : "http://www.scottish.parliament.uk/images/MSP%20Photos/GordonMacDonaldMSP.jpg",
'Ken Macintosh' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853527816.jpg",
'Mike MacKenzie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853509411.jpg",
'Jenny Mara' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853514522.jpg",
'Tricia Marwick' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders/TriciaMarwickMSP.jpg",
'Stewart Maxwell' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853518144.jpg",
'Margaret McCulloch' : "http://www.scottish.parliament.uk/images/MSP%20Photos/McCullochMargaret.jpg",
'Mark McDonald': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853521925.jpg",
'Margaret McDougall' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853521965.jpg",
'Jamie McGrigor' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853522127.jpg",
'Alison McInnes' : "http://www.scottish.parliament.uk/images/MSP%20Photos/AlisonMcinnes_20130522.jpg",
'Fiona McLeod' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853524252.jpg",
'Michael McMahon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525411.jpg",
'Siobhan McMahon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525209.jpg",
'Stuart McMillan' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525711.jpg",
'Elaine Murray': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853530243.jpg",
'Alex Neil' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853531419.jpg",
'Gil Paterson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853534583.jpg",
'Graeme Pearson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853536823.jpg",
'Willie Rennie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853537139.jpg",
'Michael Russell': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853541633.jpg",
'Alex Salmond' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SalmondAlexIG.jpg",
'Mary Scanlon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853619775.jpg",
'John Scott' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853619194.jpg",
'Travish Scott' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853620466.jpg",
'Richard Simpson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853629298.jpg",
'Drew Smith' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SmithDrewIG.jpg",
'Liz Smith' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SmithLizIG.jpg",
'Stewart Stevenson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853634458.jpg",
'David Stewart' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853635694.jpg",
'Kevin Stewart' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853636994.jpg",
'Nicola Sturgeon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853640645.jpg",
'Dave Thompson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_11405270866.jpg",
'Paul Wheelhouse' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853652552.jpg",
'Sandra White' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853653523.jpg",
'Humza Yousaf' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853621795.jpg"
}

# cabinet here http://en.wikipedia.org/wiki/Scottish_Government#Ministers
# TO DO: more jobs
# TO TO: think how to have a history of jobs
jobs = [
['Alex', 'Salmond', 'First Minister', parser.parse('16 May 2007').date, parser.parse('20 November 2014').date()],
['Nicola', 'Sturgeon', 'First Minister', parser.parse('20 November 2014').date(), parser.parse('5 May 2016').date()],
['Tricia', 'Marwick', 'Presiding Officer', parser.parse('11 May 2011').date(), parser.parse('5 May 2016').date()],
['Joe', 'Fitzpatrick', 'Minister for Parliamentary business', parser.parse('5 September 2012').date(), parser.parse('5 May 2016').date()],
['Elaine', 'Smith', 'Deputy Presiding Officer', parser.parse('11 May 2011').date(), parser.parse('5 May 2016').date()],
['John', 'Scott', 'Deputy Presiding Officer', parser.parse('11 May 2011').date(), parser.parse('5 May 2016').date()],
['John', 'Swinney', 'Cabinet Secretary for Finance, Constitution and Economy', parser.parse('21 November 2014').date(),parser.parse('5 May 2016').date()],
['Alasdair', 'Allan', 'Minister for Learning, Science and Scotland\'s Languages', parser.parse('7 December 2011').date(),parser.parse('5 May 2016').date()],
['Angela', 'Constance', 'Minister for Youth Employment', parser.parse('7 December 2011').date(),parser.parse('22 April 2014').date()]
]

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
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i, status=MSP.MEMBER,         # basic data, sufficient to run visualisations & website
                    member_startdate = parser.parse('5 May 2011').date(), member_enddate = parser.parse('5 May 2016').date(),   # (as they should allow nulls for other fields)
                    party_startdate = parser.parse('5 May 2011').date(), party_enddate = parser.parse('5 May 2016').date())     # default ranges, will be overwritten for the few msps that move about
            m.save()

# no longer members, but were in this session
def add_other_msps():
    m = MSP(firstname='Brian', lastname='Adam', constituency=Constituency.objects.get(name='Aberdeen Donside'),
            member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse(' 25 April 2013'),
            party=Party.objects.get(name='Scottish National Party'),
            party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('25 April 2013'),
            status=MSP.DECEASED, foreignid=129,)
    m.save()
    m = MSP(firstname='Helen', lastname='Eadie', constituency=Constituency.objects.get(name='Cowdenbeath'),
            member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse('9 November 2013'),
            party=Party.objects.get(name='Scottish Labour'),
            party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('9 November 2013'),
            status=MSP.DECEASED, foreignid=130)
    m.save()
    m = MSP(firstname='Margo', lastname='MacDonald', constituency=Constituency.objects.get(name='Lothian'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('4 April 2014'),
            party=Party.objects.get(name='Independent'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('4 April 2014'),
            status=MSP.DECEASED, foreignid=131)
    m.save()
    m = MSP(firstname='David', lastname='McLetchie', constituency=Constituency.objects.get(name='Lothian'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('12 August 2013'),
            party=Party.objects.get(name='Scottish Conservative and Unionist Party'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('12 August 2013'),
            status=MSP.DECEASED, foreignid=132)
    m.save()
    m = MSP(firstname='John', lastname='Park', constituency=Constituency.objects.get(name='Mid Scotland and Fife'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('9 November 2013'),
            party=Party.objects.get(name='Scottish Labour'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('9 November 2013'),
            status=MSP.RESIGNED, foreignid=133)
    m.save()
    m = MSP(firstname='Bill', lastname='Walker', constituency=Constituency.objects.get(name='Dunfermline'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse(' 9 September 2013'),
            party=Party.objects.get(name='Independent'),
            party_startdate = parser.parse('3 March 2012'), party_enddate = parser.parse(' 9 September 2013'),
            status=MSP.RESIGNED, foreignid=134)
    m.save()

# Should populate with data for msps that move about
# def update_transient_msps():

def msp_photos():
    msps = MSP.objects.all()
    for msp in msps:
        name = str(msp)
        if name in msp_img_urls.keys():
            msp.img = msp_img_urls[name]
            msp.save()

def msp_jobs():
    for job in jobs:
        j = Job(name=job[2],msp=MSP.objects.get(firstname=job[0], lastname=job[1]),startdate=job[3],enddate=job[4])
        j.save()

def populate_votes(files):
    # naive skip files before 06 May 2011, using a switch: currentsession
    # change encouraged
    currentsession = False
    for f in files[:85]:
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

def rebellious_votes():

    divisions = Division.objects.all()
    parties = Party.objects.all()

    # That means taking into account the dates between which he was a member -- for the latest party??
    # TO DO: exclude independent??

    # Check if a vote is rebellious
    for party in parties:
        party_msps = MSP.objects.filter(party = party)
        threshold = (len(party_msps))/2
        for division in divisions[:20]:
            print division
            division_votes = Vote.objects.filter(division = division)
            relevant_votes = [vote for vote in division_votes if vote.msp in party_msps]
            votes = [0, 0, 0, 0, 0]
            votes[1] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.YES) if vote.msp in party_msps])
            votes[2] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.NO) if vote.msp in party_msps])
            votes[3] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSTAIN) if vote.msp in party_msps])
            votes[4] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSENT) if vote.msp in party_msps])
            max = 4
            if votes[1]>threshold:
                max = 1
            elif votes[2]>threshold:
                max = 2
            elif votes[3]>threshold:
                max = 3
            if max == 2 or max == 3:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.YES) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 2:
                        vote.party_vote = Vote.NO
                    else:
                        vote.party_vote = Vote.ABSTAIN
                    vote.save()
            if max == 1 or max == 3:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.NO) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 1:
                        vote.party_vote = Vote.YES
                    else:
                        vote.party_vote = Vote.ABSTAIN
                    vote.save()
            if max == 1 or max == 2:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSTAIN) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 1:
                        vote.party_vote = Vote.YES
                    else:
                        vote.party_vote = Vote.NO
                    vote.save()



def compute_turnout():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # Get all the absent votes to compute turnout
    for division in divisions:
        votes_divison = Vote.objects.filter(division=division)
        msps_absent = set(msps)
        for vote in votes_divison:
            msps_absent = [msp for msp in msps_absent if msp!= vote.msp]
        for msp in msps_absent:
            v = Vote(msp = msp, division = division, vote = Vote.ABSENT)
            v.save()
        division.turnout =  Decimal(129 - len(msps_absent)) * 100 /Decimal(129)
        division.save()

def compute_rebels():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # rebels for each division
    for division in divisions:
        division.rebels = len(Vote.objects.filter(division = division, rebellious = True))
        division.save()

    # compute presence and rebellions
    # TO DO : instead of len(divisions) consider the actual set of divisions where he could have been present
    for msp in msps:
        votes_present = len(divisions) - len(Vote.objects.filter(msp=msp, vote=Vote.ABSENT))
        if votes_present > 0 :
            msp.rebellions = Decimal(len(Vote.objects.filter(msp=msp, rebellious=True))) * 100 / Decimal(votes_present)
        msp.presence = votes_present * 100 / Decimal(len(divisions))
        msp.save()

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
#    update_transient_msps()
#    print "_update_"
    msp_photos()
    print "_photos_"
    msp_jobs()
    print "_jobs_"
    populate_votes(get_files('../scraper/report_scraper/data/'))
    print "_votes_"
    rebellious_votes()
    print "_rebellious_votes_"
    compute_turnout()
    print "_turnout_"
    compute_rebels()
    print "_rebels_"
    print "_done_"
