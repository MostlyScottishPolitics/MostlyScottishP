from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from msp import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'scottviz.views.home', name='home'),
                       # url(r'^scottviz/', include('scottviz.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
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


                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
