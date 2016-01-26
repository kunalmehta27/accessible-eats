#!/usr/bin/python
# -*- encoding: utf-8-*-

from django.core.management.base import BaseCommand
from accessible_eats_app.helpers import text_to_object

class Command(BaseCommand):

    def handle(self, *args, **options):
        twitter_cron()


def twitter_cron():
	restaurant_obj = text_to_object('Leals 79124')
	print restaurant_obj