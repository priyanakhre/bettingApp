import json
from django.shortcuts import render
import urllib.request
import urllib.parse
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def create_user(request):
    data = {
        "first_name": request.POST.get("first_name", ""),
        "last_name": request.POST.get("last_name", ""),
        "username": request.POST.get("username", ""),
        "password": request.POST.get("password", "")
    }
    endpoint = models_endpoint+ 'user/'
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(endpoint, data=data_encoded, method='POST')
    raw = urllib.request.urlopen(request).read().decode('utf-8')
    create = json.loads(raw)
    return JsonResponse(create)
    

@csrf_exempt
def login(request):
    if request.method != "POST":
        return exp_response(False, "Must Be POST")
    data = {
        "username": request.POST.get("username", ""),
        "password": request.POST.get("password", "")
    }
    endpoint = models_endpoint+ 'user/authenticate/'
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(endpoint, data=data_encoded, method='POST')
    raw = urllib.request.urlopen(request).read().decode('utf-8')
    login = json.loads(raw)
    return JsonResponse(login)

@csrf_exempt
def logout(request):
    if request.method != "POST":
        return exp_response(False, "Must be a POST request")

    data = {
        "auth_token": request.COOKIES.get('auth_token', '')
    }

    endpoint = models_endpoint+ 'authenticators/delete'
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(endpoint, data=data_encoded, method='POST')
    raw = urllib.request.urlopen(request).read().decode('utf-8')
    logout = json.loads(raw)
    return JsonResponse(logout)

@csrf_exempt
def create_bet(request):
    data = {

        "privacy": request.POST.get("privacy", ""),
        "response_limit":request.POST.get("response_limit", ""),
        "category": request.POST.get("category", ""),
        "question": request.POST.get("question", ""),
        "description": request.POST.get("description", ""),
        "min_buyin" :request.POST.get("min_buyin", ""),
        "per_person_cap":request.POST.get("per_person_cap", ""),
        "initiation": request.POST.get("initiation", ""),
        "expiration":request.POST.get("expiration", ""),
        "auth_token":request.POST.get("auth_token", "")

    
    }
    endpoint = models_endpoint+ 'bet/'
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(endpoint, data=data_encoded, method='POST')
    raw = urllib.request.urlopen(request).read().decode('utf-8')
    create_user = json.loads(raw)
    return JsonResponse(create_user)

def check_authenticator(request):
    endpoint = models_endpoint+ 'authenticators/check/'
    data_encoded = urllib.parse.urlencode(request.GET).encode('utf-8')
    request = urllib.request.Request(endpoint, data=data_encoded, method='POST')
    raw = urllib.request.urlopen(request).read().decode('utf-8')
    check_auth = json.loads(raw)
    return JsonResponse(check_auth)
