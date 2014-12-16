import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scottviz.settings")
from collections import OrderedDict
import csv

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from models import *

from search import postcode_search, model_search
from scatter.get_votes_for_scatter import get_votes_for_scatter
from scatter.write_scatter import write_scatter
from scatter.get_data_scatter import get_data_scatter
from scatter.run_pca import run_pca

from django.utils.safestring import mark_safe



navbar = (

    ('msps', {'id': 'msps', 'title': 'MSPs', 'desc': 'List of all Members of Scottish Parliament'}),

    # ("regions", {
    #        'id': 'regions',
    #        'title': 'Regions',
    #        'desc': 'List of all regions in Scotland',
    #    }),

    ('divisions', {
        'id': 'divisions',
        'title': 'Divisions',
        'desc': 'List of all votes in the Parliament'
    }),

    ('map', {
        'id': 'map',
        'title': 'Map',
        'desc': 'Interactive map of scottish regions',
    }),

    ('topics', {
        'id': 'topics',
        'title': 'Topics',
        'desc': 'Browse topics and divisions related to them'
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

scatter = {'pca': {
    'id': 'pca',
    'title': 'PCA',
    'desc': 'PCA visualisation of MSPs based on their votes',
}
}
about = OrderedDict(about)
navbar = OrderedDict(navbar)
content = {
    'title': "MSP",
    'copyr': "Team C 2014",
    'contact_name': "Team C",
    'contact_email': "1006414v@student.gla.ac.uk",
    'navbar': navbar,
    'scatter': scatter,
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
    content["divisions"] = Division.objects.order_by('-date')[:10]

    return render_to_response('index.html', content, context)

@cache_page(60 * 15)
def map(request):
    """
    map view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['map']
    return render_to_response('map.html', content, context)


def pca(request):
    """
    PCA view
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = scatter['pca']
    reusable_query = Topic.objects.all().order_by('id')
    content['parties'] = Party.objects.all().order_by('id')
    content['topics'] = reusable_query
    content['selected_topics'] = []
    parties = []
    topics = []
    if request.method == 'POST':
        query = request.POST
        if query.getlist('party'):
            parties = query.getlist('party')
        if query.getlist('topic'):
            topics = query.getlist('topic')
        votes = get_votes_for_scatter(parties,topics)
        scores = run_pca(votes)
        write_scatter(scores)
        content['data'] = mark_safe(get_data_scatter(scores))
        return HttpResponse()
    else:
    # FOR THE CONCURRENCY
    # You want to find the 'freshest' which you have not responded to
    # either by timestamp and keeping a record of what you responded to
    # or by having an extra field where you record the answer to requests
        votes = get_votes_for_scatter(parties,topics)
        scores = run_pca(votes)
        write_scatter(scores)
        content['data'] = get_data_scatter(scores)
        return render_to_response('pca.html', content, context)


def msps(request):
    """
    msps view -- gets all msps from db ordered by lastname first, then firstname
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['msps']
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    content['count'] = MSP.objects.count()
    return render_to_response('msps.html', content, context)


@cache_page(60 * 15)
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
    rebellious = Vote.objects.filter(msp=this_msp, rebellious=True).select_related('vote')
    content['rebellions'] = rebellious
    content['for'] = rebellious.filter(vote=Vote.YES)
    content['against'] = rebellious.filter(vote=Vote.NO)
    content['abstain'] = rebellious.filter(vote=Vote.ABSTAIN)
    content['absent'] = rebellious.filter(vote=Vote.ABSENT)
    content['party_for'] = rebellious.filter(party_vote=Vote.YES)
    content['party_against'] = rebellious.filter(party_vote=Vote.NO)
    content['party_abstain'] = rebellious.filter( party_vote=Vote.ABSTAIN)
    content['party_absent'] = rebellious.filter(party_vote=Vote.ABSENT)
    content['attendance'] = Vote.objects.filter(msp=this_msp).exclude(vote=Vote.ABSENT).order_by('division')
    return render_to_response('msp.html', content, context)


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
    content['party'] = this_party
    content['partymsps'] = MSP.objects.filter(party=this_party).order_by('lastname','firstname')
    return render_to_response('party.html', content, context)


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
    return render_to_response('regions.html', content, context)


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
    constituency_msps = MSP.objects.filter(constituency=this_constituency)
    parent_msps = []
    kids = []
    if this_constituency.parent is not None:
        parent_msps = MSP.objects.filter(constituency=this_constituency.parent)
    else:
        kids = Constituency.objects.filter(parent=this_constituency)
    content['constituency'] = this_constituency
    content['constituency_msps'] = constituency_msps
    content['parent_msps'] = parent_msps
    content['constituencies'] = kids
    return render_to_response('constituency.html', content, context)


@cache_page(60 * 15)
def divisions(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['divisions']
    content['divisions'] = Division.objects.order_by('-date')
    content['count'] = Division.objects.count()
    return render_to_response('divisions.html', content, context)


@cache_page(60 * 15)
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
    content['rebels'] = Vote.objects.filter(division=this_division, rebellious=True).order_by('msp')
    content['votes'] = Vote.objects.filter(division=this_division).order_by('msp')
    content['analytics'] = Analytics.objects.filter(division=this_division).order_by('party')
    q = Division.objects.filter(motionid__startswith=this_division.motionid.split('.')[0])
    content['related'] = q.exclude(motionid__exact=this_division.motionid).order_by('motionid')
    return render_to_response('division.html', content, context)

@cache_page(60 * 15)
def topics(request):
    """
    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = navbar['topics']
    results = []
    topics = Topic.objects.all().order_by('name')
    for topic in topics:
        divisions = Division.objects.filter(topic=topic.id).order_by('-date')
        results.append([topic, len(divisions), divisions])
    content['topics'] = results
    return render_to_response('topics.html', content, context)


def aboutus(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = about['aboutus']
    return render_to_response('aboutus.html', content, context)


def aboutsp(request):
    """

    :param request:
    :return:
    """
    context = RequestContext(request)
    content['activesite'] = about['aboutsp']
    return render_to_response('aboutsp.html', content, context)


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
            entry_query = model_search.get_query(query, ['motionid', 'motiontopic', 'motiontext', ])
            content['divisions'] = Division.objects.filter(entry_query)
            entry_query = model_search.get_query(query, ['name', ])
            content['regions'] = Constituency.objects.filter(entry_query)
            entry_query = model_search.get_query(query, ['name', ])
            content['parties'] = Party.objects.filter(entry_query)

    return render_to_response('search_results.html', content, context)


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
            writer.writerow([div.motionid, div.parent, div.date, None, div.motiontopic, div.motiontext, div.result, div.link])
    elif thing == "msps":
        msps = MSP.objects.order_by('lastname')
        writer = csv.writer(response)
        writer.writerow(["Name", "Status", "MSP From", "MSP Until", "Party", "Party Member From", "Party Member Until",
                         "Constituency", "Presence", "Rebellions"])
        for msp in msps:
            writer.writerow([msp.__unicode__(), msp.status, msp.member_startdate, msp.member_enddate, msp.party,
                             msp.party_startdate, msp.party_enddate, msp.constituency, msp.presence, msp.rebellions])
    return response

