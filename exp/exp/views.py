import json
from django.shortcuts import render
import urllib.request
import urllib.parse
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.conf import settings
from datetime import datetime

models_endpoint = 'http://models-api:8000/api/v1/'

def exp_response(success, payload):
    return JsonResponse({'success': success, 'data': payload})

def all_bets(request):
    req = urllib.request.Request(models_endpoint+'bet/')
    raw = urllib.request.urlopen(req).read().decode('utf-8')
    bets_json = json.loads(raw)

    if bets_json['success']:
        return exp_response(True, bets_json['data'])
    else:
        return exp_response(False, bets_json['data'])

def recent_bets(request, count):
    req = urllib.request.Request(models_endpoint + 'bet/')
    raw = urllib.request.urlopen(req).read().decode('utf-8')
    bets_json = json.loads(raw)

    recent = []
    if bets_json['success']:
        for i in range(int(count)):
            if i < len(dict(bets_json)['data']):
                recent.append(dict(bets_json)['data'][i])
        return exp_response(True, bets_json)
    else:
        return exp_response(False, bets_json['data'])

def all_categories(request):
    req = urllib.request.Request(models_endpoint + 'bet/')
    raw = urllib.request.urlopen(req).read().decode('utf-8')
    bets_json = json.loads(raw)

    categories = []
    if bets_json['success']:
        for bet in dict(bets_json)['data']:
            cat = (dict(bet))['category']
            if cat not in categories:
                categories.append(cat)
        return exp_response(True, categories)
    else:
        return exp_response(False, bets_json['data'])


def bet_detail(request, bet_id):
    url = urllib.request.Request(models_endpoint+'bet/' + bet_id + '/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    bet_json = json.loads(raw)

    if bet_json['success']:
        return exp_response(True, bet_json['data'])
    else:
        return exp_response(False, bet_json['data'])

def bet_responses(request, bet_id):
    url = urllib.request.Request(models_endpoint + 'bet/' + bet_id + '/responses/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    responses_json = json.loads(raw)

    if responses_json['success']:
        return exp_response(True, responses_json['data'])
    else:
        return exp_response(False, responses_json['data'])

def response_detail(request, response_id):
    url = urllib.request.Request(models_endpoint + 'response/' + response_id + '/')
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    response_json = json.loads(raw)

    if response_json['success']:
        return exp_response(True, response_json['data'])
    else:
        return exp_response(False, response_json['data'])
