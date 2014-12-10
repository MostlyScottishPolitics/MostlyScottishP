from collections import OrderedDict
import csv

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from Spviz.scottviz import postcode_search, model_search
from models import *
from decimal import *

navbar = (

    ('msps', {'id': 'msps', 'title': 'MSPs', 'desc': 'List of all Members of Scottish Parliament'}),

    ("regions", {
        'id': 'regions',
        'title': 'Regions',
        'desc': 'List of all regions in Scotland',
    }),

    ('divisions', {
        'id': 'divisions',
        'title': 'Divisions',
        'desc': 'List of all votes in the Parliament'
    }),

    ('map', {
        'id': 'map',
        'title': 'Map',
        'desc': 'map visualisation',
    }),

    ('scatter', {
        'id': 'scatter',
        'title': 'Scatter',
        'desc': 'MSPs are plotted based on their votes',
    }),

    ('map', {
        'id': 'map',
        'title': 'Map',
        'desc': 'map visualisation',
    }),

    ('scatter', {
        'id': 'scatter',
        'title': 'Scatter',
        'desc': 'MSPs are plotted based on their votes',
    })
)

about = (
    ('aboutus', {
        'id': 'aboutus',
        'title': 'About us',
        'desc': 'About this project',
    }),

    ('aboutsp', {
        'id': 'aboutsp',
        'title': 'About the Scottish Parliament',
        'desc': 'About the MSPs and their votes',
    })

)

about = OrderedDict(about)
navbar = OrderedDict(navbar)

content = {
    'title': "Mostly Scottish Politics",
    'copyr': "Team C 2014",
    'contact_name': "Team C",
    'contact_email': "1006414v@student.gla.ac.uk",
    'navbar': navbar,
    'about': about,
}


def home(request):
    """
    home view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = {
        'id': 'home',
        'title': 'Welcome to Mostly Scottish Politics(MSP)',
        'desc': "Browse motions, regions, MSPs, see how they vote, and don't forget to have a go at our interactive visualisations and map ",
    }
    return render_to_response('scottviz_app/base.html', content, context)


def map(request):
    """
    map view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['map']
    return render_to_response('scottviz_app/map.html', content, context)


def scatter(request):
    """
    PCA view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['scatter']
    return render_to_response('scottviz_app/scatter.html', content, context)


def msps(request):
    """
    msps view -- gets all msps from db ordered by lastname first, then firstname
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['msps']
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    return render_to_response('scottviz_app/msps.html', content, context)


def msp(request, mspID):
    """
    view for a particular msp -- gets specific msp info from db, plus attendance and rebellions
    :param request:
    :param mspID:
    :return:
    """
    context = RequestContext(request)
    this_msp = MSP.objects.get(foreignid=mspID)
    content['activesite'] = {
        'id': this_msp.foreignid,
        'title': this_msp.firstname + " " + this_msp.lastname,
        'desc': "Voting record for " + this_msp.firstname + " " + this_msp.lastname,
    }
    content['msp'] = this_msp
    content['msp'].votecount = Vote.objects.filter(msp=this_msp).count()
    content['jobs'] = Job.objects.filter(msp=this_msp)
    content['rebellions'] = Vote.objects.filter(msp=this_msp, rebellious=True)
    content['for'] = Vote.objects.filter(msp=this_msp, rebellious=True, vote=Vote.YES)
    content['against'] = Vote.objects.filter(msp=this_msp, rebellious=True, vote=Vote.NO)
    content['abstain'] = Vote.objects.filter(msp=this_msp, rebellious=True, vote=Vote.ABSTAIN)
    content['absent'] = Vote.objects.filter(msp=this_msp, rebellious=True, vote=Vote.ABSENT)
    content['party_for'] = Vote.objects.filter(msp=this_msp, rebellious=True, party_vote=Vote.YES)
    content['party_against'] = Vote.objects.filter(msp=this_msp, rebellious=True, party_vote=Vote.NO)
    content['party_abstain'] = Vote.objects.filter(msp=this_msp, rebellious=True, party_vote=Vote.ABSTAIN)
    content['party_absent'] = Vote.objects.filter(msp=this_msp, rebellious=True, party_vote=Vote.ABSENT)
    content['attendance'] = Vote.objects.filter(msp=this_msp).exclude(vote=Vote.ABSENT).order_by('division')
    return render_to_response('scottviz_app/msp.html', content, context)


def party(request, partyID):
    """
    view for a specfic party -- gets all party members from db
    :param request:
    :param partyID:
    :return:
    """
    context = RequestContext(request)
    this_party = Party.objects.get(id=partyID)
    content['activesite'] = {
        'id': this_party.id,
        'title': this_party.name,
        'desc': "Members for the " + this_party.name,
    }
    party_msps = MSP.objects.filter(party=this_party).order_by('lastname')
    content['party'] = this_party
    content['partymsps'] = party_msps
    return render_to_response('scottviz_app/party.html', content, context)


def regions(request):
    """
    regions & constituencies view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['regions']
    const = Constituency.objects.filter(parent=None).order_by('name')
    content['regions'] = const[1:]
    content['region'] = const[0]
    content['constituencies'] = Constituency.objects.exclude(parent=None).order_by('name')
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    return render_to_response('scottviz_app/regions.html', content, context)


def constituency(request, constituencyID):
    """

    :param request:
    :param constituencyID:
    :return:
    """
    context = RequestContext(request)
    this_constituency = Constituency.objects.get(id=constituencyID)
    content['activesite'] = {
        'id': this_constituency.id,
        'title': this_constituency.name,
        'desc': "Representatives for " + this_constituency.name,
    }
    constituency_msps = MSP.objects.filter(constituency=this_constituency).order_by('party')
    content['constituency'] = this_constituency
    content['constituency_msps'] = constituency_msps
    return render_to_response('scottviz_app/constituency.html', content, context)


def divisions(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['divisions']
    content['divisions'] = Division.objects.order_by('-date')
    return render_to_response('scottviz_app/divisions.html', content, context)


def division(request, divisionID):
    """

    :param request:
    :param divisionID:
    :return:
    """
    context = RequestContext(request)
    this_division = Division.objects.get(id=divisionID)
    content['activesite'] = {
        'id': this_division.motionid,
        'title': this_division.motionid,
        'desc': "More info on division " + this_division.motionid,
    }

    content['division'] = this_division
    content['votes'] = Vote.objects.filter(division=this_division).order_by('msp')
    content['rebels'] = Vote.objects.filter(division=this_division, rebellious=True)
    content['for'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.YES)
    content['against'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.NO)
    content['abstain'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.ABSTAIN)
    content['absent'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.ABSENT)
    content['party_for'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.YES)
    content['party_against'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.NO)
    content['party_abstain'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.ABSTAIN)
    content['party_absent'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.ABSENT)
    parties = Party.objects.all().order_by('name')
    results = []
    TWOPLACES = Decimal(10) ** -2
    for party in parties:
        expressed_votes = len([vote for vote in Vote.objects.filter(division=this_division).exclude(vote=Vote.ABSENT) if vote.msp.party == party])
        if expressed_votes>0:
            pro = Decimal(Decimal(100*len([vote for vote in Vote.objects.filter(division=this_division, vote=Vote.YES) if vote.msp.party == party]))/Decimal(expressed_votes)).quantize(TWOPLACES)
            con = Decimal(Decimal(100*len([vote for vote in Vote.objects.filter(division=this_division, vote=Vote.NO) if vote.msp.party == party]))/Decimal(expressed_votes)).quantize(TWOPLACES)
        else:
            pro = 0
            con = 0
        turnout = Decimal(Decimal(100*expressed_votes)/Decimal(len(MSP.objects.filter(party=party)))).quantize(TWOPLACES)
        results.append([party,pro,con,turnout])
    q = Division.objects.filter(motionid__startswith=this_division.motionid.split('.')[0])
    print this_division.motionid.split('.')[0]
    content['related'] = q.exclude(motionid__exact=this_division.motionid)
    content['parties'] = parties
    content['results'] = results
    return render_to_response('scottviz_app/division.html', content, context)


def rebels(request, divisionID):
    """

    :param request:
    :param divisionID:
    :return:
    """
    context = RequestContext(request)
    this_division = Division.objects.get(id=divisionID)
    content['activesite'] = {
        'id': this_division,
        'title': this_division,
        'desc': "Rebels of " + str(this_division),
    }
    content['division'] = this_division
    content['rebels'] = Vote.objects.filter(division=this_division, rebellious=True)
    content['for'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.YES)
    content['against'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.NO)
    content['abstain'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.ABSTAIN)
    content['absent'] = Vote.objects.filter(division=this_division, rebellious=True, vote=Vote.ABSENT)
    content['party_for'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.YES)
    content['party_against'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.NO)
    content['party_abstain'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.ABSTAIN)
    content['party_absent'] = Vote.objects.filter(division=this_division, rebellious=True, party_vote=Vote.ABSENT)
    return render_to_response('scottviz_app/rebels.html', content, context)


def aboutus(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = about['aboutus']
    return render_to_response('scottviz_app/aboutus.html', content, context)


def aboutsp(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = about['aboutsp']
    return render_to_response('scottviz_app/aboutsp.html', content, context)


def search_results(request):
    """
    search for postcode, Msp -- name, Division -- id, topic, text, Constituency and Party
    :param request:
    :return:
    """
    context = RequestContext(request)
    query = request.GET['q']
    content['activesite'] = {
        'id': 'search',
        'title': '',
        'desc': 'Results for: ' + query,
        }
    content['postcode'] = {}
    content['msps'] = {}
    content['divisions'] = {}
    content['regions'] = {}
    content['parties'] = {}

    if ('q' in request.GET) and request.GET['q'].strip():
        if postcode_search.is_valid(query):
            results = postcode_search.get_msps(query)
            content['postcode'] = results
        else:
            entry_query = model_search.get_query(query, ['firstname', 'lastname', ])
            content['msps'] = MSP.objects.filter(entry_query)
            entry_query = model_search.get_query(query, ['motionid', 'topic', 'motiontext', ])
            content['divisions'] = Division.objects.filter(entry_query)
            entry_query = model_search.get_query(query, ['name', ])
            content['regions'] = Constituency.objects.filter(entry_query)
            entry_query = model_search.get_query(query, ['name', ])
            content['parties'] = Party.objects.filter(entry_query)

    return render_to_response('scottviz_app/search_results.html', content, context)


def export_csv(request, thing):
    """
    creates and returns a csv file with either msps or divisions
    :param request:
    :param thing:
    :return:
    """
    thing.strip()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + thing + '".csv"'

    if thing == "divisions":
        divs = Division.objects.order_by('-date')
        writer = csv.writer(response)
        writer.writerow(["Motion id", "Parent", "Date", "Proposed by", "Topic", "Description", "Result", "Link"])
        for div in divs:
            writer.writerow([div.motionid, div.parent, div.date, None, div.topic, div.motiontext, div.result, div.link])
    elif thing == "msps":
        msps = MSP.objects.order_by('lastname')
        writer = csv.writer(response)
        writer.writerow(["Name", "Party", "Constituency"])
        for msp in msps:
            writer.writerow([msp.__unicode__(), msp.party, msp.constituency])
    return response
