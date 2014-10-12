from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from collections import OrderedDict


navbar=(
	('index', {
				'id':'index',
				'title':'Home', 
				'desc': "Front page",
	}), 

	('msps', {
				'id':'msps',
				'title':'MSPs', 
				'desc': 'List of all Members of Scottish Parliament',
	}),

	('regions', {
				'id': 'regions',
				'title':'Regions', 
				'desc': 'List of all regions and constituencies in Scotland',
	}),

	('parties', {
				'id': 'parties',
				'title':'Parties', 
				'desc': 'List of all parties and their members'
	}),

	('divisions', {
				'id': 'divisions',
				'title':'Divisions', 
				'desc': 'List of all votes in the Parliament'
	})
)

navbar = OrderedDict(navbar)
print navbar
content={
	'title': "MSP visualization tool",
	'copyr': "Team C 2014",
	'contact_name': "Team C",
	'contact_email': "1006414v@student.gla.ac.uk",
	'navbar': navbar,
}


def index(request):
	context = RequestContext(request)
	content['activesite'] = navbar['index']
	return render_to_response('scottviz_app/base.html', content, context)


def msps(request):
	context = RequestContext(request)
	content['activesite'] = navbar['msps']
	return render_to_response('scottviz_app/msps.html', content, context)


def msp(request,mspID):
	context = RequestContext(request)
	return render_to_response('scottviz_app/msp.html', content, context)


def parties(request):
	context = RequestContext(request)
	content['activesite'] = navbar['parties']
	return render_to_response('scottviz_app/parties.html', content, context)


def party(request,partyID):
	context = RequestContext(request)
	return render_to_response('scottviz_app/party.html', content, context)


def regions(request):
	context = RequestContext(request)
	content['activesite'] = navbar['regions']		
	return render_to_response('scottviz_app/regions.html', content, context)


def region(request,regionID):
	context = RequestContext(request)
	return render_to_response('scottviz_app/region.html', content, context)

def divisions(request):
	context = RequestContext(request)
	content['activesite'] = navbar['divisions']		
	return render_to_response('scottviz_app/divisions.html', content, context)


def division(request,regionID):
	context = RequestContext(request)
	return render_to_response('scottviz_app/division.html', content, context)



