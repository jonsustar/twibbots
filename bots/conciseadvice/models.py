from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re
from twibbots.bots.base.models import *
from twibbots.manager.models import *
from twibbots.twitter.models import *

BOT_NAME = 'conciseadvice'

class Bot(BaseBot):
    bot_name = BOT_NAME
    
    def process_tweet(self, tweet):
        print "PROCESSING TWEET"
        
        return Tweet()

class Rule(BaseRule):
    bot_name = BOT_NAME