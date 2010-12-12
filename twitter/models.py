from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re

from django.db.models.fields import IntegerField
from django.conf import settings

BOT_STATUS_CHOICES = (('debug','debug'), ('active','active'), ('disabled','disabled'))
TWEET_TYPE_CHOICES = (('test','test'), ('actual','actual'))

class BigIntegerField(IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"
    def db_type(self):
        return 'bigint' # Note this won't work with Oracle.

'''
class TwitterUser(models.Model):
    twitter_id =  models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.username
          
    def Search(twitter_username):
        db_user, user_created = TwitterUser.objects.get_or_create(username=twitter_username)
        db_user.save()
        return db_user
        
    Search = staticmethod(Search)
'''
class Conversation(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(blank=False,null=False)

    def get_tweets(self):
        tweets = self.tweet_set.order_by('created_at')
        return tweets

class Tweet(models.Model):
    status_id = BigIntegerField()
    from_rest_id = BigIntegerField(blank=True, null=True)
    from_search_id = BigIntegerField(blank=True, null=True)
    from_username = models.CharField(max_length=30)
    to_rest_id = BigIntegerField(blank=True, null=True)
    to_search_id = BigIntegerField(blank=True, null=True)
    to_username = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=200)
    in_reply_to_status_id = BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TWEET_TYPE_CHOICES, default="actual")
    language = models.CharField(max_length=2, default="en")
    conversation = models.ForeignKey(Conversation, blank=True, null=True)
    
    def __unicode__(self):
        return self.from_username + ": " + self.text
    
    def get_formatted_text(self):
        text = self.text
        text = re.sub(r'@(\w+)', r'<a target="_blank" href="http://twitter.com/\1">@\1</a>', text)
        return text
    
    def get_twitter_url(self):
        return "http://twitter.com/" + self.from_username + "/status/" + str(self.twitter_id)
    
    def get_retweet_url(self):
        tweet_content = "RT @" + self.from_username + ": " + self.text
        tweet_content = tweet_content.replace(" ","%20")
        return "http://twitter.com/home?status=" + tweet_content
        
    def Search(tweet):
        db_tweet, tweet_created = Tweet.objects.get_or_create(status_id=tweet.id, from_search_id=tweet.from_user_id, from_username=tweet.from_user, to_search_id=tweet.to_user_id, created_at=tweet.created_at, text=tweet.text, language=tweet.iso_language_code)
        if tweet_created:
            return db_tweet
        else:
            return None
            
    Search = staticmethod(Search)
    