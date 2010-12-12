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
        consumer_token = "KALkUmw13ZaXdsXHOT5SQ"
        consumer_secret = "MtNSzay6FvDxK5lKbcM5gDjF9Jz3U5g7ZURyGBNkWFM"
        
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        
        '''
        try:
            redirect_url = auth.get_authorization_url()
            print redirect_url
        except tweepy.TweepError:
            print 'Error! Failed to get request token.'
            
        verifier = raw_input('Verifier:')
        
        try:
            auth.get_access_token(verifier)
            print "SUCCESS"
            print "KEY: " + auth.access_token.key
            print "SECRET: " + auth.access_token.secret
        except tweepy.TweepError:
            print 'Error! Failed to get access token.'
            
        # for conciseadvice:
        # key: 80658421-fIMM55xHQPHNvf8N0AmEOoMWntFwQgB97adSIjtja
        # secret: bC4H3BW2luMwDbQGiqmpGnWXiCuv9HihxTl1fKEgmjs
        
        '''
        
        key = "80658421-fIMM55xHQPHNvf8N0AmEOoMWntFwQgB97adSIjtja"
        secret = "bC4H3BW2luMwDbQGiqmpGnWXiCuv9HihxTl1fKEgmjs"
        
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
                