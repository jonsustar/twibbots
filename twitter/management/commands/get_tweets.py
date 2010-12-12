from django.core.management.base import NoArgsCommand
import tweepy
import warnings
from twibbots.twitter.models import *

class Command(NoArgsCommand):
    help = "Set-up and initialize a website"
    def handle_noargs(self, **options):
        
        '''
        public_tweets = tweepy.api.public_timeline()
        for tweet in public_tweets:
            print tweet.text
            
        print "TRY AUTHORIZATION ---------"
        '''

        
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        tweets = api.search('"need advice" OR "what do you think"',"en")
        for tweet in tweets:
            print tweet.text
            saved_tweet = Tweet.Search(tweet)
            if saved_tweet is not None:
                saved_tweet.save()
                print "-- Save successful"
            else:
                print "-- Save failed"
                