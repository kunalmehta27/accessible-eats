#!/usr/bin/python
# -*- encoding: utf-8-*-

from django.core.management.base import BaseCommand
from accessible_eats_app.helpers import parse_yelp_obj
from yelpapi import YelpAPI

yelp_api = YelpAPI('US2mtMpskJ36JSb_n6Uy-w', 'gtu09XfGR3FwC_Ar7LLYGEB-3EM', 'fIvJ3B48nF_Ro6QP5C-m6ptJOQHB5p7u', '8lApWweZlez8vmlBYQ5mNMW3pWI')

class Command(BaseCommand):

    def handle(self, *args, **options):
        update()


def update():
	restaurants = Restaurant.objects.all()
	for restaurant in restaurant:
		search_results = yelp_api.search_query(id=restaurant.yelp_id)
		yelp_restaurant_object = search_results['businesses'][0]
		restaurant = parse_yelp_obj(yelp_restaurant_object, restaurant)
		restaurant.save()