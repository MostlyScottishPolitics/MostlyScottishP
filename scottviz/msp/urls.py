from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^msps/', views.msps, name='msps'),
                       url(r'^msp/(?P<mspID>\w+)/$', views.msp, name='msp'),
                       url(r'^party/(?P<partyID>\w+)/$', views.party, name='party'),
                       url(r'^constituency/(?P<constituencyID>\w+)/$', views.constituency, name='constituency'),
                       url(r'^division/(?P<divisionID>\w+)/$', views.division, name='division'),
                       url(r'^export_csv/(?P<thing>\w+)/$', views.export_csv, name='export_csv'),
                       #url(r'^regions/', views.regions, name='regions'),
                       url(r'^divisions/', views.divisions, name='divisions'),
                       url(r'^aboutus/', views.aboutus, name='aboutus'),
                       url(r'^aboutsp/', views.aboutsp, name='aboutsp'),
                       url(r'^map/', views.map, name='map'),
                       url(r'^pca/', views.pca, name='pca'),
                       url(r'^search_results/', views.search_results, name='search_results'),
                       url(r'^topics/', views.topics, name='topics'),


)