from django.conf.urls import patterns, url

from scottviz_app import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^msps/', views.msps, name='msps'),
                       # url(r'^msp/(?P<mspID>\w+)/$', views.msp, name = 'msp'),
                       #	url(r'^party/(?P<partyID>\w+)/$',views.party,name = 'party'),
                       #	url(r'^region/(?P<regionID>\w+)/$',views.region,name='region'),
                       url(r'^parties/', views.parties, name='parties'),
                       url(r'^constituencies/', views.constituencies, name='constituencies'),
                       url(r'^regions/', views.regions, name='regions'),
                       url(r'^divisions/', views.divisions, name='divisions'),
                       url(r'^mspsviz/', views.msps, name='msps'),
                       url(r'^partiesviz/', views.parties, name='parties'),
                       url(r'^constituenciesviz/', views.constituencies, name='constituencies'),
                       url(r'^regionsviz/', views.regions, name='regions'),
                       url(r'^divisionsviz/', views.divisions, name='divisions'),
                       url(r'^aboutus/', views.aboutus, name='aboutus'),
                       url(r'^aboutsp/', views.aboutsp, name='aboutsp'),
                       url(r'^search_results/', views.search_results, name='search_results'),

)