from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response
import csv
from django.http import HttpResponse
from scottviz_app import postcode_search
from models import *

navbar = (

    ('msps', {'id': 'msps', 'title': 'MSPs', 'desc': 'List of all Members of Scottish Parliament'}),

    # ("constituencies", {
    # 'id': 'constituencies',
    # 'title': 'Constituencies',
    # 'desc': 'List of all constituencies in Scotland',
    # }),

    ("regions", {
        'id': 'regions',
        'title': 'Regions',
        'desc': 'List of all regions in Scotland',
    }),

    # ('parties', {
    #    'id': 'parties',
    #    'title': 'Parties',
    #    'desc': 'List of all parties and their members'
    #}),

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
        'desc': 'Scatter plot',
    })
)

navbarviz = (

    ('map', {
        'id': 'map',
        'title': 'Map',
        'desc': 'map visualisation',
    }),

    ('scatter', {
        'id': 'scatter',
        'title': 'Scatter',
        'desc': 'Scatter plot',
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
navbarviz = OrderedDict(navbarviz)

content = {
    'title': "Mostly Scottish Politics",
    'copyr': "Team C 2014",
    'contact_name': "Team C",
    'contact_email': "1006414v@student.gla.ac.uk",
    'navbarviz': navbarviz,
    'navbar': navbar,
    'about': about,
}


def home(request):
    context = RequestContext(request)
    content['activesite'] = {
    'id': 'home',
    'title': 'Welcome to Mostly Scottish Politics(MSP)',
    'desc': "Browse motions, regions, MSPs, see how they vote, and don't forget to have a go at out interactive visualisations and map ",
}
    return render_to_response('scottviz_app/base.html', content, context)


def map(request):
    context = RequestContext(request)
    content['activesite'] = navbarviz['map']
    return render_to_response('scottviz_app/map.html', content, context)


def scatter(request):
    context = RequestContext(request)
    content['activesite'] = navbarviz['scatter']
    return render_to_response('scottviz_app/scatter.html', content, context)


def msps(request):
    context = RequestContext(request)
    content['activesite'] = navbar['msps']
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    return render_to_response('scottviz_app/msps.html', content, context)


def msp(request, mspID):
    context = RequestContext(request)
    this_msp = MSP.objects.get(foreignid=mspID)
    content['activesite'] ={
    'id': this_msp.foreignid,
    'title': this_msp.firstname + " " + this_msp.lastname,
    'desc': "Voting record for "+ this_msp.firstname + " " + this_msp.lastname,
    }
    content['msp'] = this_msp
    content['msp'].votecount = Vote.objects.filter(msp=this_msp).count()
    return render_to_response('scottviz_app/msp.html', content, context)


"""
def parties(request):
    context = RequestContext(request)
    content['activesite'] = navbar['parties']
    content['parties'] = Party.objects.order_by('name')
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    return render_to_response('scottviz_app/parties.html', content, context)


def constituencies(request):
    context = RequestContext(request)
    content['activesite'] = navbar['constituencies']
    content['constituencies'] = Constituency.objects.exclude(parent=None).order_by('name')
    content['msps'] = MSP.objects.all()
    return render_to_response('scottviz_app/constituencies.html', content, context)
"""


def party(request, partyID):
    context = RequestContext(request)
    this_party = Party.objects.get(id=partyID)
    content['activesite'] ={
    'id': this_party.id,
    'title': this_party.name,
    'desc': "Members for the " + this_party.name,
    }
    party_msps = MSP.objects.filter(party=this_party).order_by('lastname')
    content['party'] = this_party
    content['partymsps'] = party_msps
    return render_to_response('scottviz_app/party.html', content, context)


def regions(request):
    context = RequestContext(request)
    content['activesite'] = navbar['regions']
    const = Constituency.objects.filter(parent=None).order_by('name')
    content['regions'] = const[1:]
    content['region'] = const[0]
    content['constituencies'] = Constituency.objects.exclude(parent=None).order_by('name')
    content['msps'] = MSP.objects.order_by('lastname', 'firstname')
    return render_to_response('scottviz_app/regions.html', content, context)


def constituency(request, constituencyID):
    context = RequestContext(request)
    this_constituency = Constituency.objects.get(id=constituencyID)
    content['activesite'] ={
    'id': this_constituency.id,
    'title': this_constituency.name,
    'desc': "Representatives for " + this_constituency.name,
    }
    constituency_msps = MSP.objects.filter(constituency=this_constituency).order_by('party')
    content['constituency'] = this_constituency
    content['constituency_msps'] = constituency_msps
    return render_to_response('scottviz_app/constituency.html', content, context)


def divisions(request):
    context = RequestContext(request)
    content['activesite'] = navbar['divisions']
    content['divisions'] = Division.objects.order_by('-date')
    return render_to_response('scottviz_app/divisions.html', content, context)


def division(request, divisionID):
    context = RequestContext(request)
    this_division = Division.objects.get(id=divisionID)
    content['activesite'] ={
    'id': this_division.motionid,
    'title': this_division.motionid,
    'desc': "More info on division " + this_division.motionid,
    }
    division_msps = MSP.objects.filter(division=this_division).order_by('motionid')
    content['division'] = this_division
    content['division_msps'] = division_msps
    return render_to_response('scottviz_app/division.html', content, context)


def aboutus(request):
    context = RequestContext(request)
    content['activesite'] = about['aboutus']
    return render_to_response('scottviz_app/aboutus.html', content, context)


def aboutsp(request):
    context = RequestContext(request)
    content['activesite'] = about['aboutsp']
    return render_to_response('scottviz_app/aboutsp.html', content, context)


def search_results(request):
    context = RequestContext(request)
    query = request.GET.get('q')
    if query:
        results = postcode_search.get_msps(query)
        content['dict'] = results
    else:
        return render_to_response('scottviz_app/base.html', content, context)
    return render_to_response('scottviz_app/search_results.html', content, context)


def export_csv(request, thing):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+thing+'".csv"'

    if thing == "divisions":
        divs = Division.objects.order_by('-date')
        writer = csv.writer(response)
        writer.writerow(["Motion id", "Parent", "Date", "Proposed by", "Topic", "Description", "Result", "Link"])
        for div in divs:
            writer.writerow([div.motionid, div.parent, div.date, None, div.topic, div.motiontext, div.result, div.link])
    elif thing =="msps":
        msps = MSP.objects.order_by('lastname')
        writer = csv.writer(response)
        writer.writerow(["Name", "Party", "Constituency"])
        for msp in msps:
            writer.writerow([msp.__unicode__(), msp.party, msp.constituency])
    return response