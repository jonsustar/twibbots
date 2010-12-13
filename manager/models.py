from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re
import tweepy

class BotDefinition(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    ordinal = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    oath_consumer_token = models.CharField(max_length=100, blank=True, null=True)
    oath_consumer_secret = models.CharField(max_length=100, blank=True, null=True)
    oath_key = models.CharField(max_length=100, blank=True, null=True)
    oath_secret = models.CharField(max_length=100, blank=True, null=True)
    tweepy_api = None
    
    def __unicode__(self):
        return self.name
    
    def get_search_definitions(self):
        return self.searchdefinition_set.all()
        
    def get_bot(self):
        instance_name = "twibbots.bots." + self.name.lower() + ".models"
        instance_import = __import__(instance_name)
        instance = sys.modules[instance_name]
        return instance.Bot()
        
    def get_tweepy_api(self):
        if self.tweepy_api is None:
            auth = tweepy.OAuthHandler(self.oath_consumer_token, self.oath_consumer_secret)
            auth.set_access_token(self.oath_key, self.oath_secret)
            self.tweepy_api = tweepy.API(auth)
        return self.tweepy_api
    
class SearchDefinition(models.Model):
    bot_definition = models.ForeignKey(BotDefinition)
    query = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.query