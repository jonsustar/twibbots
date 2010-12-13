from django.core.management.base import NoArgsCommand
import tweepy
import warnings
from twibbots.twitter.models import *
from twibbots.manager.models import *

class Command(NoArgsCommand):
    help = "Set-up and initialize a website"
    def handle_noargs(self, **options):
        
        for bot_definition in BotDefinition.objects.all():    
            for search_definition in bot_definition.get_search_definitions():
                tweets = bot_definition.get_tweepy_api().search(search_definition.query,"en")
                for tweet in tweets:
                    original_tweet = Tweet.Search(tweet)
                    if original_tweet is not None:
                        reply_tweet = bot_definition.get_bot().process_tweet(original_tweet)
                        if reply_tweet is not None:
                            print reply_tweet
                            #original_tweet.save()
                        else:
                            print "NO REPLY"
                        print "--------------------"
        '''
        public_tweets = tweepy.api.public_timeline()
        for tweet in public_tweets:
            print tweet.text
            
        print "TRY AUTHORIZATION ---------"
        '''

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
        
        '''
        
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
        '''