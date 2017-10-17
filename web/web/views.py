import urllib.request
import urllib.parse
from django.shortcuts import render, Http404
from django.urls import reverse
import json
from .forms import RegisterForm, LoginForm, CreateBetForm
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpRequest

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

    auth = request.COOKIES.get('auth_token')
    if not auth:
        return render(request, 'home/index.html', context)
    else: 
        context["message"] = "You Are Logged In!"
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




def create_account(request):
    auth = request.COOKIES.get('auth_token')
    if auth:
        return HttpResponseRedirect(reverse('web-index'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, 'home/register.html', {'form': form, 'message': "Your Passwords do not match"})
            data = {}
            data["first_name"] = form.cleaned_data["first_name"]
            data["last_name"] = form.cleaned_data["last_name"]
            data['username'] = form.cleaned_data["username"]
            data['password'] = form.cleaned_data["password"]
            data_encoded = urllib.parse.urlencode(data).encode('utf-8')
            req_url = urllib.request.Request(exp_endpoint + "user/create", data=data_encoded, method='POST')
            raw = urllib.request.urlopen(req_url).read().decode('utf-8')
            res = json.loads(raw)

            if not res or res['success'] == False:
                return render(request, 'home/register.html', {'form': form, 'message': res['data']})
            else:
                try:
                    response = HttpResponseRedirect('/login/')
                    return response
                except Exception as e:
                    return render(request, 'home/register.html', {'form': form, 'message': str(e)})
        else:
            return render(request, 'home/register.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()
        return render(request, 'home/register.html', {'form': form})

@csrf_exempt
def logout(request):
    auth = request.COOKIES.get('auth_token')
    if not auth:
        
        return HttpResponseRedirect(reverse('login'))
    response = HttpResponseRedirect(reverse('web-index'))
    response.delete_cookie("auth_token")

    data = {}
    data["auth_token"] = auth
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    req_url = urllib.request.Request(exp_endpoint + "accounts/logout/", data=data_encoded, method='POST')
    raw = urllib.request.urlopen(req_url).read().decode('utf-8')
    res = json.loads(raw)

    
    return response



@csrf_exempt
def login(request):
    auth = request.COOKIES.get('auth_token')
    if auth:
        return HttpResponseRedirect(reverse('web-index'))

    if request.method == 'GET':
        # return a blank form
        login_form = LoginForm()
        return render(request, 'home/login.html', {'form': login_form, 'auth_token': auth})


    
    f = LoginForm(request.POST)
    if not f.is_valid():
        # invalid form
           
        # show errors and take them back to the login page
        return render(request, 'home/login.html', {'message': "Please fill out all fields", 'form': f})
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']
    data = {}
    data['username'] = username
    data['password'] = password
    # submit request to exp layer
    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    req_url = urllib.request.Request(exp_endpoint + "accounts/login/", data=data_encoded, method='POST')
    raw = urllib.request.urlopen(req_url).read().decode('utf-8')
    response = json.loads(raw)


    if not response['success']:
        # an error occurred
        # show errors and take them back to the login page
        return render(request, 'home/login.html', {'message': response["data"], 'form': f})
    # made it this far, so they can log in
    auth_token = response['data']['auth_token']
    login_form = LoginForm()
        # show errors and take them back to the login page
    #return render(request, 'home/login.html', {'message': 'auth token is ' + auth_token, 'form': login_form})
    next = HttpResponseRedirect(reverse('web-index'))
    next.set_cookie('auth_token', auth_token)
    return next


def create_bet(request):
    auth = request.COOKIES.get('auth_token')
    if not auth:
        return HttpResponseRedirect(reverse('login'))
    # what kind of request?
    if request.method == 'GET':
        form = CreateBetForm()
        return render(request, 'home/create_bet.html', {'form': form, 'auth_token': auth})
    else:
        form = CreateBetForm(request.POST)
        if not form.is_valid():
            form = CreateBetForm()
            return render(request, 'home/create_bet.html', {'form': form, 'auth_token': auth, 'msg': 'Invalid information provided.'})

        # get clean info

        privacy = form.cleaned_data['privacy']
        response_limit = form.cleaned_data['response_limit']
        category = form.cleaned_data['category']
        question = form.cleaned_data['question']
        description = form.cleaned_data['description']
        min_buyin = form.cleaned_data['min_buyin']
        per_person_cap = form.cleaned_data['per_person_cap']
        expiration = form.cleaned_data['expiration']
        
        data = {}
        data['privacy'] = privacy
        data['response_limit'] = response_limit
        data['category'] = category
        data['question'] = question
        data['description'] = description
        data['min_buyin'] = min_buyin
        data['per_person_cap'] = per_person_cap
        data['intitiation'] = datetime.datetime.now()
        data['expiration'] = expiration
        data['auth_token'] = auth

        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req_url = urllib.request.Request(exp_endpoint + "create_bet/", data=data_encoded, method='POST')
        raw = urllib.request.urlopen(req_url).read().decode('utf-8')
        response = json.loads(raw)

        if not response['success']:
            return render(request, 'home/create_bet.html', {'message': response['data'], 'form': form, 'auth_token': auth})
        response = HttpResponseRedirect(reverse('web-index'))
        return response