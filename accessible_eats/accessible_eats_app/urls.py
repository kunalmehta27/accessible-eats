from django.conf.urls import include, url
from django.contrib import admin
from accessible_eats_app import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^review/$', views.review, name="review"),
    url(r'^search/$', views.search, name="search"),
]