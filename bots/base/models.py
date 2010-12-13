from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re
from twibbots.grammarengine.resolver import Resolver

class BaseBot():
    
    def get_resolver(self):
        resolver = Resolver()
        resolver.bot_name = self.bot_name
        return resolver
        
    def publish_tweet(self, tweet):
        print "published tweet"
        
    

class BaseRule(models.Model):
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=500)
    last_used_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.start + "|" + self.end
        
    def mark(self):
        if not self.id is not None:
            self.last_used_date = datetime.now()
            self.save()
        
    def unmark(self):
        if self.id is not None:
            self.last_used_date = None
            self.save()