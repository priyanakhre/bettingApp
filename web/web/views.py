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

    context = {}

    if all_bets['success']:
        context['all_bets'] = all_bets['data']
    else:
        return render(request, 'home/error.html', {'error':'All bets not available'})

    if all_cats['success']:
        context['all_cats'] = all_cats['data']
    else:
        return render(request, 'home/error.html', {'error':'All categories not available'})

    if recent_bets['success']:
        context['recent_bets'] = recent_bets['data']
    else:
        return render(request, 'home/error.html', {'error': 'Recent bets not available'})

    return render(request, 'home/index.html', context)


def bet_detail(request, id):
    url = urllib.request.Request(exp_endpoint + 'bet_detail/' + id + '/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    bet = json.loads(raw)

    url = urllib.request.Request(exp_endpoint + 'bet_responses/' + id + '/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    responses = json.loads(raw)

    context = {}
    context['bet'] = bet['data']

    if not bet['success']:
        return render(request, 'home/error.html', {'error':'Bet not available!'})

    if responses['success']:
        context['responses'] = responses['data']

    return render(request, 'home/bet_detail.html', context)