from scottviz import settings

__author__ = '2168879m'
"""
This file contains all the functions definition that populate fields in tables already containing minimal data
Mostly processes the data in the tables to populate fields with analytics
I strongly encourage you to put any such definitions here, and the appropriate calls in updatedb.py
All static data comes from data.py, please put any such data there.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from msp.models import *
from decimal import *
from data import number_of_msps, independent_parties, topics_divisions, topic_extracter_name, topic_extracter_location, \
    topics, party_links_colours
import importlib
from django.core.files import File

# the definitions here can be changed to get other statistics


def get_map_csv():
    with open(settings.STATIC_PATH + '/csv/map_data.csv', 'w') as f:
        myFile = File(f)
        header = 'Region,id'
        parties = Party.objects.all().order_by('id')
        for party in parties:
            header += ',' + party.name
        myFile.write(header)

        regions = Constituency.objects.filter(parent=None)
        for region in regions:
            myFile.write('\n' + str(region.name))
            myFile.write(',' + str(region.id))
            for party in parties:
                constituencies = Constituency.objects.filter(parent=region)
                result = len([msp for msp in MSP.objects.filter(party=party) if msp.constituency in constituencies])
                myFile.write(',' + str(result))


def get_parties_colors_csv():
    with open(settings.STATIC_PATH+'/csv/parties_colors.csv','w') as f:
        myFile = File(f)
        header = 'Party,Color'
        myFile.write(header)
        parties = Party.objects.all().order_by('id')
        for party in parties:
            myFile.write('\n' + str(party.name))
            myFile.write(',' + str(party.colour))

def compute_division_turnout():
    """
    For all divisions computes turnout
    :return: populate turnout field in division table
    """
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # we have more msps in the db  (dead,resigned)
    error = len(msps) - number_of_msps

    # turnout for each division
    for division in divisions:
        absentVotes = Vote.objects.filter(division=division, vote=Vote.ABSENT)
        division.turnout = Decimal(number_of_msps - len(absentVotes)) * 100 / Decimal(number_of_msps)
        division.save()


def compute_msp_turnout():
    """
    For all msps computes turnout
    :return: populate presence field in MSP table
    """
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
    """
    for all divisions adds the rebelious votes
    :return: populates the rebels field in division table
    """
    divisions = Division.objects.all()

    # rebels for each division
    for division in divisions:
        division.rebels = len(Vote.objects.filter(division=division, rebellious=True))
        division.save()


def compute_msp_rebellions():
    """
    for all msps adds their rebelious votes and weights it using presence, to get a percentage
    :return: populates the rebellions field in MSP table
    """
    alldivisions = len(Division.objects.all())
    msps = MSP.objects.all()

    # rebellions for each msp
    for msp in msps:
        # if msp.presence already computed :
        if msp.presence and alldivisions:
            msp.rebellions = 10000 * Decimal(len(Vote.objects.filter(msp=msp, rebellious=True))) / (
                msp.presence * alldivisions)
            msp.save()

            # otherwise, comment the previous 2 lines and uncomment the next 4 lines:
            #
            # votes_present = len(divisions) - len(Vote.objects.filter(msp=msp, vote=Vote.ABSENT))
            # if votes_present > 0 :
            # msp.rebellions = Decimal(len(Vote.objects.filter(msp=msp, rebellious=True))) * 100 / Decimal(votes_present)
            # msp.save()


def independent_party_rebellious_votes(parties):
    """
    For all given parties (assumed independent), marks all votes as non-rebellious
    - since there is no-one to rebel against
    :param parties: list/set of Party instances
    :return: populates, for all given parties, rebellious field for vote with False
    """

    # MSPs for independent cannot make rebellious votes
    votes = Vote.objects.all()
    for vote in votes:
        if vote.msp.party in parties:
            vote.rebellious = False
            vote.save()

            # alternative code that seems of greater complexity, maybe test for time?
            # for each vote for each msp for each independent party
            # for party in parties:
            # party_msps = MSP.objects.filter(party = party)
            #   for msp in party_msps:
            #       votes = Vote.objects.all(msp = msp)
            #       for vote in votes:
            #           vote.rebellious = False
            #           vote.save()


# do not change, helper function
def put(votes_list, party_vote, rebellious):
    """
    for all given votes in the votes_list, puts the given values in the relevant fields
    :param votes_list: a list/set of Vote instances
    :param party_vote: a vote type (Vote.YES, Vote.NO, Vote.ABSTAIN, Vote.ABSENT)
    :param rebellious: a vote type (Vote.YES, Vote.NO, Vote.ABSTAIN, Vote.ABSENT)
    :return: populates the party_vote and rebellious fields of vote table, for the given votes
    """
    for vote in votes_list:
        vote.party_vote = party_vote
        vote.rebellious = rebellious
        vote.save()


def not_independent_party_rebellious_votes(parties):
    """
    For all given parties (assumed not independent), for all divisions, gets the majoritary party vote
    and for all votes for that join, populates the Vote fields accordingly
    :param parties: list/set of Party instances
    :return: populates, for all given parties, rebellious and party_vote fields for Vote table
    """

    divisions = Division.objects.all()
    # Check if a vote for msps in not independent parties is rebellious
    for party in parties:
        for division in divisions:
            expressed_votes_from_party = len(
                [vote for vote in Vote.objects.filter(division=division).exclude(vote=Vote.ABSENT) if
                 vote.msp.party == party])
            threshold = (expressed_votes_from_party + 1) / 2
            # get all the votes for this division
            division_votes = Vote.objects.filter(division=division)
            # split the votes by vote
            votes_yes = [vote for vote in division_votes.filter(vote=Vote.YES) if vote.msp.party == party]
            votes_no = [vote for vote in division_votes.filter(vote=Vote.NO) if vote.msp.party == party]
            votes_abstain = [vote for vote in division_votes.filter(vote=Vote.ABSTAIN) if vote.msp.party == party]
            votes_absent = [vote for vote in division_votes.filter(vote=Vote.ABSENT) if vote.msp.party == party]
            # decide a party vote if threshold reached
            # and put the results in
            if len(votes_yes) > threshold:
                put(votes_yes, Vote.YES, False)
                put(votes_no, Vote.YES, True)
                put(votes_abstain, Vote.YES, True)
                put(votes_absent, Vote.YES, False)
            elif len(votes_no) > threshold:
                put(votes_yes, Vote.NO, True)
                put(votes_no, Vote.NO, False)
                put(votes_abstain, Vote.NO, True)
                put(votes_absent, Vote.NO, False)
            elif len(votes_abstain) > threshold:
                put(votes_yes, Vote.ABSTAIN, True)
                put(votes_no, Vote.ABSTAIN, True)
                put(votes_abstain, Vote.ABSTAIN, False)
                put(votes_absent, Vote.ABSTAIN, False)
            else:
                put(votes_yes, Vote.ABSENT, False)
                put(votes_no, Vote.ABSENT, False)
                put(votes_abstain, Vote.ABSENT, False)
                put(votes_absent, Vote.ABSENT, False)


def compute_rebellious_votes():
    """
    Splits the parties in Party into independent and not-independent (based on static list in data.py)
     and makes the appropriate calls to populate the fields
    :return: populates party_vote and rebellious fields in Vote table
    """
    parties = Party.objects.all()

    # get a list of not independent parties:
    notindparties = parties
    for party in independent_parties:
        notindparties = notindparties.exclude(name__exact=party)
    # compute for not independent parties
    not_independent_party_rebellious_votes(notindparties)

    # get a list of independent parties
    indparties = parties
    for party in parties:
        indparties = indparties.exclude(id=party.id)
    # compute for independent parties
    independent_party_rebellious_votes(indparties)


def compute_type_for_divisions():
    """
    Gets the type
    :return: populates the type field in Division table
    """
    divisions = Division.objects.all()

    for division in divisions:
        if '.' in division.motionid:
            division.motion = False
        else:
            division.motion = True
        division.save()


def compute_parents_for_divisions():
    """
    Assumes the type field is already populated and looks for immediate parent of a division (based on motionid field)
    :return: populates parent field in Division table
    """

    divisions = Division.objects.all()

    for division in divisions:
        if not division.motion:
            ammend_length = 1 + len(division.motionid.split('.')[-1:])
            parent = Division.objects.filter(motionid__exact=division.motionid[:-ammend_length])
            if len(parent) > 1:
                print 'We found a duplicate entry for this motion: ' + parent[0].motionid
                print 'More info:'
                for p in parent:
                    print p.motionid + ' with id ' + str(p.id) + ' on date ' + str(p.date)
            else:
                for p in parent:
                    division.parent = p
                division.save()


def get_parents_topic(division):
    """
    Helper function
    :param division: a division instance
    :return: the topic of the most ancient parent we can find
    """
    if (not division.motion) and (division.parent):
        return get_parents_topic(division.parent)
    else:
        return Topic.objects.get(name=division.topic.name)


def compute_topics():
    """
    computes topics for the topic_divisions using a topic_extracter (all info taken from data)
    to use your own:
        change the set of topic_divisions in data
        change the topic_extracter_name and topic_extracter_location in data
    :return: populates topic field in Division table
    """

    extracter = importlib.import_module(topic_extracter_name, topic_extracter_location)

    # extract all topics as good as possible
    for division in topics_divisions:
        if division.motion:
            topic = extracter.get_topic_from_text(division.motiontext)
        else:
            topic = extracter.get_topic_from_text(division.motiontopic)
        division.topic = Topic.objects.get(name=topic)
        division.save()

    # adjust topics for ammendments
    # why not do it before? cause we can have ammendments to ammendments with no main parent, or ammendments to ammendments with parent
    for division in topics_divisions:
        if (not division.motion) and (division.parent):
            division.topic = get_parents_topic(division.parent)
            division.save()


def see_diferences_with_new_topic_extractor():
    """
    Function to test a new topic extractor by comparison.
    It works similarly to compute_topics, except:
        It does not save to db the new topics
        It prints the ones that are different (with division id and name for reference)
    You need to change the extracter_name and extracter_location in data to your own.
    :return: differences between the topics in db and new topics
    """
    extracter = importlib.import_module(topic_extracter_name, topic_extracter_location)

    # extract all topics as good as possible
    for division in topics_divisions:
        if division.motion:
            topic = extracter.get_topic_from_text(division.motiontext)
        else:
            topic = extracter.get_topic_from_text(division.motiontopic)
        if (division.topic != topic) and (not division.parent):
            if topic == None:
                print str(division.id) + ' ' + division.motionid + ' ' + division.topic + '  '
            else:
                print str(division.id) + ' ' + division.motionid + ' ' + division.topic + '  ' + topic


def populate_topics():
    """
    Populate the Topics table, needed by the scatter
    uses static data from data.py
    If you design your own topic extractor, make sure your topics and the static topics match
    :return: populates the Topics table
    """
    Topic.objects.all().delete()

    for topic, description in topics.items():
        t = Topic(name=topic, description=description)
        t.save()


def populate_data_parties():
    """
    uses static data from data.py
    :return: populates link and description fields in Party table
    """

    for party, (link, description, description_link, colour) in party_links_colours.items():
        p = Party.objects.get(name=party)
        p.link = link
        p.description = description.decode('latin1')
        p.description_link = description_link
        p.colour = colour
        p.save()


def populate_analytics():
    """
    For the party by vote tab, in the division page
    :return: populates the Analytics table
    """
    Analytics.objects.all().delete()

    parties = Party.objects.all().exclude(name__startswith='No Party').order_by('name')
    divisions = Division.objects.all()

    for division in divisions:
        TWOPLACES = Decimal(10) ** -2
        for party in parties:
            a = Analytics(division=division, party=party)
            expressed_votes = len([vote for vote in Vote.objects.filter(division=division).exclude(vote=Vote.ABSENT) if
                                   vote.msp.party == party])
            if expressed_votes > 0:
                a.party_for = Decimal(100 * len(
                    [vote for vote in Vote.objects.filter(division=division, vote=Vote.YES) if
                     vote.msp.party == party]) / Decimal(expressed_votes)).quantize(TWOPLACES)
                a.party_against = Decimal(100 * len(
                    [vote for vote in Vote.objects.filter(division=division, vote=Vote.NO) if
                     vote.msp.party == party]) / Decimal(expressed_votes)).quantize(TWOPLACES)
            else:
                a.party_for = 0
                a.party_against = 0
            a.party_turnout = Decimal((100 * expressed_votes) / Decimal(len(MSP.objects.filter(party=party)))).quantize(
                TWOPLACES)
            a.save()
