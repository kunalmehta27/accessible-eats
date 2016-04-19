#!/usr/bin/python
# -*- encoding: utf-8-*-

from django.core.management.base import BaseCommand
from accessible_eats_app.helpers import text_to_object
from accessible_eats_app.models import *
import tweepy
from django.conf import settings
from pyshorteners import Shortener

import warnings
warnings.filterwarnings("ignore")

class Command(BaseCommand):

    def handle(self, *args, **options):
        twitter_cron()

def process_tweet(tweet):
    ae_screen_name = 'accessible_eats'
    user_screen_name = tweet.user.screen_name
    mentions = [a['screen_name'] for a  in tweet.entities['user_mentions']]
    if ae_screen_name in mentions and 'Fill out your survey' not in tweet.text:
        text = tweet.text.replace('@' + ae_screen_name, '').strip()
        restaurant_obj = text_to_object(text)
        if restaurant_obj != None:
            url = settings.CURRENT_HOST + 'survey/' + str(restaurant_obj.id) + '/'
            response = "Thanks for using Accessible Eats. Fill out your survey for " + restaurant_obj.name + " at " + url + "."
        else:
            response = "Sorry, unable to parse request. Please try again."
        return response, user_screen_name
    else:
        return None, None


def twitter_cron():
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY,settings.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    c = tweepy.Cursor(api.user_timeline, count = 200).items()
    while True:
        try:
            tweet = c.next()
            obj, created = ReviewedTweet.objects.get_or_create(tweet_id = tweet.id)
            if created:
                obj.save()
                response, user_screen_name = process_tweet(tweet)
                if response is not None:
                    status = "@%s %s" % (user_screen_name, response)
                    api.update_status(status, tweet.id)
        except StopIteration:
            break