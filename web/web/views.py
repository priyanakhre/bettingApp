#from django.shortcuts import render
import urllib.request
import urllib.parse
from django.shortcuts import render, Http404
#import requests
import json
#from json import JSONEncoder
#from django.template import loader
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpRequest
#from django.conf import settings
#from django.core.urlresolvers import reverse
#from django.contrib import messages

#def index(request):
# return HttpResponse("success")
exp_endpoint = 'http://exp-api:8000/exp/'

def index(request):
    url = urllib.request.Request(exp_endpoint+'all_bets/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    all_bets = json.loads(raw)

    url = urllib.request.Request(exp_endpoint + 'all_categories/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    all_cats = json.loads(raw)

    url = urllib.request.Request(exp_endpoint + 'recent_bets/3/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    recent_bets = json.loads(raw)

    success_context = {}
    error_context = ''

    if all_bets['success']:
        success_context['all_bets'] = all_bets['data']
    else:
        error_context = 'All bets not available'

    if all_cats['success']:
        success_context['all_cats'] = all_cats['data']
    else:
        error_context = 'All categories not available'

    if recent_bets['success']:
        success_context['recent_bets'] = recent_bets['data']
    else:
        error_context = 'Recent bets not available'

    if not (all_bets['success'] and all_cats['success'] and recent_bets['success']):
        return render(request, 'home/error.html', error_context)
    else:
        return render(request, 'home/index.html', success_context)


def bet_detail(request, id):
    url = urllib.request.Request(exp_endpoint + 'bet_detail/' + id + '/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    bet = json.loads(raw)

    if not bet['success']:
        context = 'Bet not available!'
        return render(request, 'home/error.html', context)
    else:
        return render(request, 'home/bet_detail.html', bet["data"])