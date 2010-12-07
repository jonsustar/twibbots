from twibbots.grammarengine.models import *
from django.template import Context, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404

def resolve(request):
    
    start_text = request.GET['start']
    
    tests = []
    
    name_rule = Rule(start='<TEST>',end='Jon!!!!!!!!!!!!!!!!')
    
    r = Resolver()
    r.add_temporary_rule('<TEST>','<GREETING> <NAME>!')
    r.add_temporary_rule('<NAME>','Jon')
    r.add_temporary_rule('<NAME>','Joe')
    r.add_temporary_rule('<NAME>','Bill')
    r.add_temporary_rule('<NAME>','Phil')
    
    for i in range(0,10):
        tests.append(r.resolve(start_text)) 
    
    t = loader.get_template('resolve.html')
    c = Context({
        'tests' : tests
    })
    
    return HttpResponse(t.render(c))