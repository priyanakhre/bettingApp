# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import User, Bet, Response

class ModelTests(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        pass
    #ADD checking for 
    # TESTING USER MODEL
    def test_create_user(self):
        user1 = {'first_name': 'Unlikely', 'last_name': 'Name', 'username': 'fire', 'password': 'color',
                 'num_tokens': 6, 'num_flags': 9}
        response = self.client.post(reverse('api-users'), user1).json()
        user = User.objects.filter(username='fire')
        self.assertTrue(user.exists())
        self.assertEquals(response['success'], True)

    def test_create_user_false(self):
        response = self.client.post(reverse('api-users'), {}).json()
        self.assertEquals(response['success'], False)

    def test_lookup_user(self): ##ERROR
        response = self.client.get(reverse('api-user', kwargs={'user_id': 3})).json()
        self.assertEquals(response['success'], True)

    def test_update_user(self): ##USER
        data = {'username': 'NewUsername'}
        response = self.client.post(reverse('api-user', kwargs={'user_id': 3}), data).json()
        new = self.client.get(reverse('api-user', kwargs={'user_id': 3})).json()
        user = User.objects.filter(username='NewUsername')
        self.assertTrue(user.exists())
        self.assertEquals(response['success'], True)

    def test_delete_user(self): ##ERROR
        response = self.client.delete(reverse('api-user', kwargs={'user_id': 3})).json()
        user = User.objects.filter(id=3)
        self.assertFalse(user.exists())
        self.assertEquals(response['success'], True)


    # TESTING BET MODEL
    def test_create_bet(self):
        bet = {'privacy': True, 'response_limit': 5, 'question': "will trump resign?", 'description': "unknown", "category" : "sports",
               'min_buyin': 3, 'per_person_cap': 4, 'auth_token': "d53e2f193a41aad0d0e02d3113d62335dcc5db53496dde569a2566525eadda32"}
        response = self.client.post(reverse('api-bets'), bet).json()
        bet = Bet.objects.filter(question='will trump resign?')
        self.assertTrue(bet.exists())
        self.assertEquals(response['success'], True)


    def test_lookup_bet(self): #ERROR
        bet = {'privacy': True, 'category': 'politics', 'response_limit': 5, 'question': "will trump resign?", 'description': "unknown",
               'min_buyin': 3, 'per_person_cap': 4}
        response = self.client.get(reverse('api-bet', kwargs={'bet_id':5})).json()
        self.assertEquals(response['success'], True)

    def test_update_bet(self): ##ERROR
        data = {'min_buyin': 15}
        response = self.client.post(reverse('api-bet', kwargs={'bet_id': 5}), data).json()
        bet = Bet.objects.get(id=5)
        self.assertTrue(bet.min_buyin==15)
        self.assertEquals(response['success'], True)

    def test_delete_bet(self): # ERROR 
        response = self.client.delete(reverse('api-bet', kwargs={'bet_id': 5})).json()
        bet = Bet.objects.filter(id=5)
        self.assertFalse(bet.exists())
        self.assertEquals(response['success'], True)

    def test_all_bets(self):
        response = self.client.get(reverse('api-bets')).json()
        self.assertEquals(response['success'], True)

    # TESTING RESPONSE MODEL

    def test_create_response(self): # ERROR
        data = {'user_id': 3, 'bet_id': 5, 'answer': True, 'amount': 100}
        resp = self.client.post(reverse('api-responses'), data).json()
        response = Response.objects.filter(amount=100)
        self.assertTrue(response.exists())
        self.assertEquals(resp['success'], True)

    def test_lookup_response(self): 
        resp = self.client.get(reverse('api-response', kwargs={'response_id': 1})).json()
        self.assertEquals(resp['success'], True)

    def test_delete_response(self): 
        response = self.client.delete(reverse('api-response', kwargs={'response_id': 1})).json()
        resp = Response.objects.filter(id=1)
        self.assertFalse(resp.exists())
        self.assertEquals(response['success'], True)

    def test_update_response(self): 
        data = {'answer': False}
        resp = self.client.post(reverse('api-response', kwargs={'response_id': 1}), data).json()
        response = Response.objects.get(id=1)
        self.assertTrue(response.answer==False)
        self.assertEquals(resp['success'], True)

    def test_all_responses(self):
        response = self.client.get(reverse('api-responses')).json()
        self.assertEquals(response['success'], True)

        # testing the tests


if __name__ == '__main__':
    x = ModelTests()
    x.setUp()
    x.test_create_user()
    x.test_create_user_false()
    x.test_lookup_user()
    x.test_update_user()
    x.test_delete_user()
    x.test_create_bet()
    x.test_lookup_bet()
    x.test_update_bet()
    x.test_delete_bet()
    x.test_all_bets()
    x.test_create_response()
    x.test_lookup_response()
    x.test_update_response()
    x.test_all_responses()
    x.test_delete_response()