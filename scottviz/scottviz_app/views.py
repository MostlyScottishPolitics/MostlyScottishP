from collections import OrderedDict
import csv
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from scottviz_app import postcode_search
from scottviz_app.models import (MSP, Constituency)

navbar = (
    ('index', {
        'id': 'index',
        'title': 'Home',
        'desc': "Front page",
    }),

    ('msps', {'id': 'msps', 'title': 'MSPs', 'desc': 'List of all Members of Scottish Parliament'}),

    ("constituencies", {
        'id': 'constituencies',
        'title': 'Constituencies',
        'desc': 'List of all constituencies in Scotland',
    }),

    ("regions", {
        'id': 'regions',
        'title': 'Regions',
        'desc': 'List of all regions in Scotland',
    }),

    ('parties', {
        'id': 'parties',
        'title': 'Parties',
        'desc': 'List of all parties and their members'
    }),

    ('divisions', {
        'id': 'divisions',
        'title': 'Divisions',
        'desc': 'List of all votes in the Parliament'
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


def index(request):
    context = RequestContext(request)
    content['activesite'] = navbar['index']
    return render_to_response('scottviz_app/base.html', content, context)


def msps(request):
    context = RequestContext(request)
    content['activesite'] = navbar['msps']
#    dict = {}
#    with open('../scraper/msp_scraper/msps.csv', mode='r') as infile:
#        reader = csv.reader(infile)
#        for row in reader:
#            row = row[0].split(';')
#            dict[row[0] + " " + row[1]] = (row[2], row[3])
#    sorted_dict = OrderedDict({})
#    for key in sorted(dict.keys()):
#        sorted_dict[key] = dict[key]
    content['dict'] = {'msps': MSP.objects.all()}
    return render_to_response('scottviz_app/msps.html', content, context)


def msp(request, mspID):
    context = RequestContext(request)
    return render_to_response('scottviz_app/msp.html', content, context)


def parties(request):
    context = RequestContext(request)
    content['activesite'] = navbar['parties']
    return render_to_response('scottviz_app/parties.html', content, context)


def party(request, partyID):
    context = RequestContext(request)
    return render_to_response('scottviz_app/party.html', content, context)


def constituencies(request):
    context = RequestContext(request)
    content['activesite'] = navbar['constituencies']
    content['dict'] = {'constituencies': Constituency.objects.exclude(parent=None).order_by('name')}
    return render_to_response('scottviz_app/constituencies.html', content, context)

def regions(request):
    context = RequestContext(request)
    content['activesite'] = navbar['regions']
    content['dict'] = {'regions': Constituency.objects.filter(parent=None).order_by('name')}
    return render_to_response('scottviz_app/regions.html', content, context)

def constituency(request, regionID):
    context = RequestContext(request)
    return render_to_response('scottviz_app/constituency.html', content, context)


def divisions(request):
    context = RequestContext(request)
    content['activesite'] = navbar['divisions']
    return render_to_response('scottviz_app/divisions.html', content, context)


def division(request, regionID):
    context = RequestContext(request)
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

