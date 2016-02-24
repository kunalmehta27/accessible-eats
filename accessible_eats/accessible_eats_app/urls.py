from django.conf.urls import include, url
from django.contrib import admin
from accessible_eats_app import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^review/$', views.review, name="review"),
    url(r'^search/$', views.search, name="search"),
url(r'^searchresults/(?P<page_num>[0-9]+)/(?P<name>.*)/(?P<category>.*)/(?P<yelp_rating>.*)/(?P<ae_rating>[0-9]+)/(?P<filter_vals>.*)/(?P<lat>.*)/(?P<lng>.*)/(?P<location_name>.*)/$', views.searchresults, name="searchresults"),
]