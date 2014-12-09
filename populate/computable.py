__author__ = '2168879m'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spviz.scottviz.scottviz.settings")
from Spviz.scottviz.scottviz_app.models import *
from decimal import *
from data import number_of_msps, independent_parties

# the definitions here can be changed to get other statistics


def compute_division_turnout():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # we have more msps in the db  (dead,resigned)
    error = len(msps) - number_of_msps

    # turnout for each division
    for division in divisions:
        absentVotes = Vote.objects.filter(division=division, vote=Vote.ABSENT)
        division.turnout = Decimal(number_of_msps - len(absentVotes)) * 100 /Decimal(number_of_msps)
        division.save()

def compute_msp_turnout():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # turnout for each msps
    # computed over all divisions
    # one might want to compute it over the divisions on dates when the msp was a member
    # that would give more appropriate presence percentages
    # but not meaningful to compare with scatter
    for msp in msps:
        presentDivisions = len(divisions) - len(Vote.objects.filter(msp=msp, vote=Vote.ABSENT))
        msp.presence = presentDivisions * 100 / Decimal(len(divisions))
        msp.save()


def compute_division_rebels():
    divisions = Division.objects.all()

    # rebels for each division
    for division in divisions:
        division.rebels = len(Vote.objects.filter(division = division, rebellious = True))
        division.save()


def compute_msp_rebellions():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # rebellions for each msp
    for msp in msps:
        # if msp.presence already computed :
        msp.rebellions = Decimal(len(Vote.objects.filter(msp=msp, rebellious=True)))*msp.presence
        msp.save()

        # otherwise, comment the previous 2 lines and uncomment the next 4 lines:
        #
        # votes_present = len(divisions) - len(Vote.objects.filter(msp=msp, vote=Vote.ABSENT))
        # if votes_present > 0 :
        #   msp.rebellions = Decimal(len(Vote.objects.filter(msp=msp, rebellious=True))) * 100 / Decimal(votes_present)
        # msp.save()

def independent_party_rebellious_votes(parties):

    # MSPs for independent cannot make rebellious votes
    votes = Vote.objects.all()
    for vote in votes:
        if vote.msp.party in parties:
            vote.rebellious = False
            vote.save()

            # alternative code that seems of greater complexity, maybe test for time?
    # for each vote for each msp for each independent party
    # for party in parties:
    #   party_msps = MSP.objects.filter(party = party)
    #   for msp in party_msps:
    #       votes = Vote.objects.all(msp = msp)
    #       for vote in votes:
    #           vote.rebellious = False
    #           vote.save()

def not_independent_party_rebellious_votes(parties):

    divisions = Division.objects.all()

    # Check if a vote for msps in not independent parties is rebellious
    for party in parties:
        party_msps = MSP.objects.filter(party=party)
        threshold = (len(party_msps))/2
        for division in divisions:
            # get all the votes for this division
            division_votes = Vote.objects.filter(division=division)
            # get all the votes by MSPs in this party
            division_votes_party = [vote for vote in division_votes if vote.msp in party_msps]
            # split the votes by vote
            votes_yes = division_votes_party.filter(vote=Vote.YES)
            votes_no = division_votes_party.filter(vote=Vote.NO)
            votes_abstain = division_votes_party.filter(vote=Vote.ABSTAIN)
            votes_absent = division_votes_party.filter(vote=Vote.ABSENT)
            # decide a party vote if threshold reached
            if len(votes_yes)>threshold:
                vote.party_vote = Vote.YES
            elif len(votes_no)>threshold:
                vote.party_vote = Vote.NO
            elif len(votes_abstain)>threshold:
                vote.party_vote = Vote.ABSTAIN
            elif len(votes_absent)>threshold:
                vote.party_vote = Vote.ABSENT
            # for each vote for this party and division, put the right tag
            for vote in division_votes_party:
                if vote.party_vote:
                    if vote.party_vote != vote.vote :
                        vote.rebellious = True
                    else:
                        vote.rebellious = False
                vote.save()

def compute_rebellious_votes():

    parties = Party.objects.all()

    # get a list of not independent parties:
    notindparties = parties
    for party in independent_parties:
        notindparties = notindparties.exclude(name__exact=party)
    # compute for not independent parties
    not_independent_party_rebellious_votes(notindparties)

    # get a list of independent parties
    indparties = parties.exclude(notindparties)
    # compute for independent parties
    independent_party_rebellious_votes(indparties)
