__author__ = '2168879m'

import os
from decimal import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")

from Spviz.scottviz.scottviz_app.models import *

def rebellious_votes():

    divisions = Division.objects.all()
    query = Party.objects.exclude(name__exact='Independent')
    parties = query.exclude(name__exact='No Party Affiliation')
    allparties = Party.objects.all()

    # That means taking into account the dates between which he was a member -- for the latest party??
    # TO DO: exclude independent??

    # Check if a vote is rebellious
    for party in allparties:
        if party in parties:
            print "ignore"
            print party
        else:
            print "Goes to 0 "
            print party
            party_msps = MSP.objects.filter(party = party)
#                print division
            this_votes = [vote for vote in Vote.objects.all() if vote.msp in party_msps]
            for vote in this_votes:
                vote.rebellious = False
                vote.save()


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

if __name__ == '__main__':
    rebellious_votes()
    print "_rebellious_votes_"
    compute_rebels()
    print "_rebels_"
    print "_done_"

