from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re

class BotDefinition(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    ordinal = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    oath_consumer_token = models.CharField(max_length=100, blank=True, null=True)
    oath_consumer_secret = models.CharField(max_length=100, blank=True, null=True)
    oath_key = models.CharField(max_length=100, blank=True, null=True)
    oath_secret = models.CharField(max_length=100, blank=True, null=True)
    
class SearchDefinition(models.Model):
    bot_definition = models.ForeignKey(BotDefinition)
    query = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
