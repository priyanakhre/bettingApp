from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import hashers
from datetime import datetime
import hashlib
import hmac
import os
import random
from django.conf import settings

from .models import User, Bet, Response, Authenticator
#229 61--check lines
def api_response(success, payload):
    return JsonResponse({'success': success, 'data': payload})

#### USER SERVICES ####

@csrf_exempt
def user_service(request, user_id=''):
    if user_id == '':
        if request.method == 'POST':
            return create_user(request)
        if request.method == 'GET':
            return get_all_users(request)
    else:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return api_response(False, 'User not found')

        if request.method == 'POST':
            return update_user(request, user)
        if request.method == 'GET':
            return get_user(request, user)
        if request.method == 'DELETE':
            return delete_user(request, user)
    return api_response(False, "Unable to process HTTP Request")

# USER - create
@csrf_exempt
def create_user(request):

    keys = ["first_name", "last_name", "username", "password", "num_tokens", "num_flags"]
    if not all(key in keys for key in request.POST.keys()):
        return api_response(False, "User not created; missing fields")

    # validation
    username = request.POST.get("username", "")
    check_user = User.objects.filter(username=username)

    if check_user.exists():
        return api_response(False, "Username Already Exists!")

    try:
        user = User(
            first_name=request.POST.get("first_name", ""),
            last_name=request.POST.get("last_name", ""),
            username=request.POST.get("username", ""),
            password=hashers.make_password(request.POST["password"]),
            num_tokens = 0,
            num_flags = 0   
        )
        user.save()
    except:
        return api_response(False, 'Could not create user')

            
    auth_token = create_authenticator(user)
    return api_response(True, "User successfully inserted into Database")
    
# USER - read
@csrf_exempt
def get_all_users(request):
    try:
        users = User.objects.all()
    except:
        return api_response(False, "Failed to find all users")
    data = [obj.as_json() for obj in users]
    return api_response(True, data)

def get_user(request, user):
    return api_response(True, user.as_json())

# USER - update
@csrf_exempt
def update_user(request, user):
    for key, value in request.POST.items():
        setattr(user, key, value)
    user.save()
    return api_response(True, 'Updated User field(s)')

# USER - delete
@csrf_exempt
def delete_user(request, user):
    try:
        user.delete()
    except:
        return api_response(False, "Unable to delete user")
    return api_response(True, 'User deleted')


#AUTHENTICATOR SERVICE



@csrf_exempt
def authenticate_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #return api_response(True, username + "cry")

    try:
        user = User.objects.get(username=username)

        pwd = user.password
        if hashers.check_password(password, pwd):
            auth_token = create_authenticator(user)
            data = {}
            data["auth_token"] = auth_token
            return api_response(True, data)
        else:
            return api_response(False, "Wrong username or password")
    except:
        return api_response(False, "Wrong Username or Password")

@csrf_exempt
def create_authenticator(user):
    
    auth_token = Authenticator.objects.filter(user_id=user)

    if auth_token.exists():
        auth_token.delete()

    
    authenticator_token= hmac.new(
        key = settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256',
    ).hexdigest()

    authenticator = Authenticator(
        authenticator = authenticator_token,
        user_id = user,
        date_created = datetime.now()
    )
    authenticator.save()
    return authenticator_token

@csrf_exempt
def check_authenticator(request):
    if request.method == "GET":
        auth_token = request.GET.get("auth_token", "")

        try:
            authenticator = Authenticator.objects.get(authenticator=auth_token)
        except:
            return api_response(False, "Enter valid authenticator")

        data = {}
        data["user_id"] = authenticator.user.id
        data["username"] = authenticator.user.username
        data["first_name"] = authenticator.user.first_name
        data["last_name"] = authenticator.user.last_name

        return api_response(True, data)
    else:
        return api_response(False, "Must Be GET")


@csrf_exempt
def delete_authenticator(request):
    if request.method == "GET":
        return api_response(False, "Must Be POST")
    if request.method == "POST":
        auth_token = request.POST["auth_token"]
        try:
            auth_token = Authenticator.objects.get(authenticator=auth_token)
            auth_token.delete()
            
        except:
            return api_response(False, "Authenticator Does Not Exist")

        return api_response(True, "Deleted Authenticator")


#### BET SERVICES ####

@csrf_exempt
def bet_service(request, bet_id=''):
    if bet_id == '':
        if request.method == 'POST':
            return create_bet(request)
        if request.method == 'GET':
            return get_all_bets(request)
    else:
        try:
            bet = Bet.objects.get(pk=bet_id)
        except Bet.DoesNotExist:
            return api_response(False, 'Bet not found')

        if request.method == 'POST':
            return update_bet(request, bet)
        if request.method == 'GET':
            return get_bet(request, bet)
        if request.method == 'DELETE':
            return delete_bet(request, bet)
    return api_response(False, "Unable to process HTTP Request")

# BET - create
@csrf_exempt
def create_bet(request):
    # validation
    try:
        authenticator = Authenticator.objects.get(authenticator=request.POST.get('auth_token', ''))
        author = authenticator.user_id
    except:
        return api_response(False, "You must be logged in to create a bet.")

    keys = ["privacy", "category", "response_limit", "question", "description", "min_buyin", "per_person_cap", "auth_token", "initiation", "expiration"]
    if not all(key in keys for key in request.POST.keys()):
        return api_response(False, "Bet not created; missing fields")

    try:
        bet = Bet(
            privacy=request.POST["privacy"],
            response_limit=request.POST["response_limit"],
            category=request.POST["category"],
            question=request.POST["question"],
            description=request.POST["description"],
            min_buyin=request.POST["min_buyin"],
            per_person_cap=request.POST["per_person_cap"]
        )
        bet.save()
        resp = {}
        resp["id"] = bet.id
    except:
        return api_response(False, 'Could not create bet')
    return api_response(True, resp)

# BET - read
@csrf_exempt
def get_all_bets(request):
    try:
        bets = Bet.objects.all()
    except:
        return api_response(False, "Failed to find all bets")
    data = [obj.as_json() for obj in bets]
    return api_response(True, data)

def get_bet(request, bet):
    return api_response(True, bet.as_json())

# BET - update
@csrf_exempt
def update_bet(request, bet):
    for key, value in request.POST.items():
        setattr(bet, key, value)
    bet.save()
    return api_response(True, 'Updated Bet field(s)')

# BET - delete
@csrf_exempt
def delete_bet(request, bet):
    try:
        bet.delete()
    except:
        return api_response(False, "Unable to delete bet")
    return api_response(True, 'Bet deleted')


#### RESPONSE SERVICES ####

@csrf_exempt
def response_service(request, response_id=''):
    if response_id == '':
        if request.method == 'POST':
            return create_response(request)
        if request.method == 'GET':
            return get_all_responses(request)
    else:
        try:
            response = Response.objects.get(pk=response_id)
        except Response.DoesNotExist:
            return api_response(False, 'Response not found')

        if request.method == 'POST':
            return update_response(request, response)
        if request.method == 'GET':
            return get_response(request, response)
        if request.method == 'DELETE':
            return delete_response(request, response)
    return api_response(False, "Unable to process HTTP Request")

# RESPONSE - create
@csrf_exempt
def create_response(request):
    # validation
    keys = ["user_id", "bet_id", "answer", "amount"]
    if not all(key in keys for key in request.POST.keys()):
        return api_response(False, "Response not created; missing fields")

    try:
        user = User.objects.get(pk=request.POST["user_id"])
    except:
        return api_response(False, 'Could not find user that wants to create response')
    try:
        bet = Bet.objects.get(pk=request.POST["bet_id"])
    except:
        return api_response(False, 'Could not find the bet this response is associated with')
    try:
        response = Response(
            user=user,
            bet=bet,
            answer=request.POST["answer"],
            amount=request.POST["amount"]
        )
        response.save()
    except:
        return api_response(False, 'Could not create response')
    return api_response(True, 'Response successfully inserted into database')

# RESPONSE - read
@csrf_exempt
def get_all_responses(request):
    try:
        responses = Response.objects.all()
    except:
        return api_response(False, "Failed to find all responses")
    data = [obj.as_json() for obj in responses]
    return api_response(True, data)

@csrf_exempt
def get_response(request, response):
    return api_response(True, response.as_json())

# RESPONSE - update
@csrf_exempt
def update_response(request, response):
    for key, value in request.POST.items():
        setattr(response, key, value)
    response.save()
    return api_response(True, 'Updated response field(s)')


# RESPONSE - delete
@csrf_exempt
def delete_response(request, response):
    try:
        response.delete()
    except:
        return api_response(False, "Unable to delete response")
    return api_response(True, 'Response deleted')

@csrf_exempt
def get_all_responses_for_bet(request, bet_id):
    if request.method == 'GET':
        try:
            bet = Bet.objects.get(pk=bet_id)
        except:
            return api_response(False, "Failed to find bet")
        try:
            responses = Response.objects.filter(bet__id=bet_id)
        except:
            return api_response(False, "Failed to find responses for this bet")
        data = [obj.as_json() for obj in responses]
        return api_response(True, data)
    else:
        return api_response(False, "Unable to process HTTP Request")

    