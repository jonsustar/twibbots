from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re

class Resolver():
    extra_rules = []
    bot_name = None
    
    def __init__(self, extra_rules=[]):
        self.extra_rules = extra_rules
        
    def get_bot_model(self):
        instance_name = "twibbots.bots." + self.bot_name + ".models"
        instance_import = __import__(instance_name)
        instance = sys.modules[instance_name]
        return instance
        
    def get_new_rule(self):
        return self.get_bot_model().Rule()
        
    def add_temporary_rule(self, start, end):
        r = self.get_new_rule()
        r.start = start
        r.end = end
        self.extra_rules.append(r)
    
    def resolve(self, starting_text):
        print starting_text
        if '<' not in starting_text:
            return starting_text
        else:
            open_index = string.find(starting_text, '<')
            close_index = string.find(starting_text, '>', open_index)
            tag = starting_text[open_index+1:close_index]
            rule_start = '<' + tag + '>'
            rule_end = self.get_end(rule_start)
            new_text = string.replace(starting_text, rule_start, rule_end, 1)
            return self.resolve(new_text)

    def get_end(self, rule_start):
        all_rules = []
        used_rules = []
        free_rules = []
        oldest_rule = None
        rule_end = ''

        all_rules = self.get_bot_model().Rule.objects.filter(start=rule_start)
        used_rules = self.get_bot_model().Rule.objects.filter(start=rule_start).exclude(last_used_date=None)

        for used_rule in used_rules:
            if type(used_rule.last_used_date) is types.UnicodeType:
                used_rule.last_used_date = datetime.strptime(used_rule.last_used_date, "%Y-%m-%d %H:%M:%S.%f")
            if oldest_rule == None or used_rule.last_used_date < oldest_rule.last_used_date:
                oldest_rule = used_rule
        rule_total = len(all_rules)
        queue_size = math.floor(rule_total * 0.7)
        if queue_size == 0:
            queue_size = 1
        used_total = len(used_rules)

        if oldest_rule != None and used_total == queue_size:
            oldest_rule.unmark()

        free_rules = list(self.get_bot_model().Rule.objects.filter(start=rule_start,last_used_date=None))
        
        for extra_rule in self.extra_rules:
            if extra_rule.start == rule_start:
                free_rules.append(extra_rule)
        
        free_total = len(free_rules)

        if free_total > 0:
            n = random.randrange(0, free_total, 1)
            rule_end = free_rules[n].end
            free_rules[n].mark()
            
        return rule_end