from django.conf.urls import patterns, url

from scottviz_app import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^msps/', views.msps, name='msps'),
                       # url(r'^msp/(?P<mspID>\w+)/$', views.msp, name = 'msp'),
                       #	url(r'^party/(?P<partyID>\w+)/$',views.party,name = 'party'),
                       #	url(r'^region/(?P<regionID>\w+)/$',views.region,name='region'),
                       url(r'^parties/', views.parties, name='parties'),
                       url(r'^constituencies/', views.constituencies, name='constituencies'),
                       url(r'^divisions/', views.divisions, name='divisions'),
                       url(r'^aboutus/', views.aboutus, name='aboutus'),
                       url(r'^aboutsp/', views.aboutsp, name='aboutsp')

)