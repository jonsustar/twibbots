from django.db import models
from datetime import datetime
import sys, sqlite3, os.path, logging, string, urllib, random, math, types, operator
import re

class Rule(models.Model):
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=500)
    last_used_date = models.DateTimeField(blank=True,null=True)

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
    
class Resolver():
    extra_rules = []
    
    def __init__(self, extra_rules=[]):
        self.extra_rules = extra_rules
        
    def add_temporary_rule(self, start, end):
        r = Rule()
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

        all_rules = Rule.objects.filter(start=rule_start)
        used_rules = Rule.objects.filter(start=rule_start).exclude(last_used_date=None)

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

        free_rules = list(Rule.objects.filter(start=rule_start,last_used_date=None))
        
        for extra_rule in self.extra_rules:
            if extra_rule.start == rule_start:
                free_rules.append(extra_rule)
        
        free_total = len(free_rules)

        if free_total > 0:
            n = random.randrange(0, free_total, 1)
            rule_end = free_rules[n].end
            free_rules[n].mark()
            
        return rule_end