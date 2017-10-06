# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import User, Bet, Response

class ModelTests(TestCase):

    def setUp(self):
        pass

    # TESTING USER MODEL
    def test_create_user(self):
        user1 = {'first_name': 'Unlikely', 'last_name': 'Name', 'username': 'fire', 'password': 'color',
                 'num_tokens': 6, 'num_flags': 9}
        response = self.client.post(reverse('api-users'), user1)
        self.assertEquals(response['success'], True)

    def test_create_user_false(self):
        response = self.client.post(reverse('api-users'), kwargs={})
        self.assertEquals(response['success'], False)

    def test_lookup_user(self):
        response = self.client.get(reverse('api-user', kwargs={'user_id': 2}))
        self.assertEquals(response['success'], True)

    def test_update_user(self):
        data = {'username': 'NewUsername'}
        response = self.client.post(reverse('api-user', kwargs={'user_id': 2}), data)
        new = self.client.get(reverse('api-user', kwargs={'user_id': 2}))
        self.assertEquals(response['success'], True)

    def test_delete_user(self):
        response = self.client.delete(reverse('api-user', kwargs={'user_id': 2}))
        self.assertEquals(response['success'], True)


    # TESTING BET MODEL
    def test_create_bet(self):
        bet = {'privacy': True, 'response_limit': 5, 'question': "will trump resign?", 'description': "unknown",
               'min_buyin': 3, 'per_person_cap': 4}
        response = self.client.get(reverse('api-bets'), bet)
        self.assertEquals(response['success'], True)

    def test_lookup_bet(self):
        bet = {'privacy': True, 'category': 'politics', 'response_limit': 5, 'question': "will trump resign?", 'description': "unknown",
               'min_buyin': 3, 'per_person_cap': 4}
        response = self.client.get(reverse('api-bet', kwargs={'bet_id':5}))
        self.assertEquals(response['success'], True)

    def test_update_bet(self):
        data = {'min_buyin': 15}
        response = self.client.post(reverse('api-bet', kwargs={'bet_id': 5}), data)
        self.assertEquals(response['success'], True)

    def test_delete_bet(self):
        response = self.client.delete(reverse('api-bet', kwargs={'bet_id': 1}))
        self.assertEquals(response['success'], True)

    def test_all_bets(self):
        response = self.client.get(reverse('api-bets'))
        self.assertEquals(response['success'], True)

    # TESTING RESPONSE MODEL

    def test_create_response(self):
        data = {'user_id': 1, 'bet_id': 1, 'answer': True, 'amount': 100}
        resp = self.client.post(reverse('api-responses', kwargs={'response_id': 5}), data)
        self.assertEquals(resp['success'], True)

    def test_lookup_response(self):
        resp = self.client.get(reverse('api-response', kwargs={'response_id': 5}))
        self.assertEquals(resp['success'], True)

    def test_delete_response(self):
        response = self.client.delete(reverse('api-response', kwargs={'response_id': 1}))
        self.assertEquals(response['success'], True)

    def test_update_response(self):
        data = {'answer': False}
        response = self.client.post(reverse('api-response', kwargs={'response_id': 5}), data)
        self.assertEquals(response['success'], True)

    def test_all_responses(self):
        response = self.client.get(reverse('api-responses'))
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


# #old code below:

# class User(unittest.TestCase):
#     def setUp(self):
#         User.objects.create(first_name="Unlikely", last_name="Name", username="fire", password="color", num_tokens=6, num_flags=9)
#         User.objects.create(first_name="Likely", last_name="Same", username="shutter", password="island", num_tokens=5, num_flags=3)

#     def test_user_calls(self):
#        	Unlikely = User.objects.get(first_name="Unlikely", last_name="Name", username="fire", password="color", num_tokens=6, num_flags=9)
#         Likely = User.objects.get(first_name="Likely", last_name="Same", username="shutter", password="island", num_tokens=5, num_flags=3)
#         self.assertEqual(Unlikely.as_json(self)[username], 'fire')
#         self.assertEqual(Unlikely.as_json(self)[num_flags], 3)
#         #could do more?

# class Bet(unittest.TestCase):
# 	def setUp(self):
#         Bet.objects.create(privacy=True, response_limit=5, question="will trump resign?", description="unknown", min_buyin=3, per_person_cap=4)
#         Bet.objects.create(privacy=True, response_limit=10, question="will the test happen?", description="known", min_buyin=5, per_person_cap=8)

#     def test_bet_call(self):
#     	Trump = User.objects.get(privacy=True, response_limit=5, question="will trump resign?", description="unknown", min_buyin=3, per_person_cap=4)
#     	The_Test = User.objects.get(privacy=True, response_limit=10, question="will the test happen?", description="known", min_buyin=5, per_person_cap=8)
#     	self.assertEqual(Trump.as_json(self)[privacy], True)
#         self.assertEqual(The_Test.as_json(self)[response_limit], 10)
#         #could do more?

# class Response(unittest.TestCase):
# 	def setUp(self):
# 		Response.objects.create(user_id=2727, bet_id=56666, answer=True, amount=100)
# 		Response.objects.create(user_id=30678, bet_id=100000, answer=False, amount=50)

# 	def test_response_call(self):
# 		Scion = Response.objects.get(user_id=2727, bet_id=56666, answer=True, amount=100)
# 		Cryon = Response.objects.get(user_id=30678, bet_id=100000, answer=False, amount=50)
# 		self.assertEqual(Scion.as_json(self)[bet_id], 56666)
# 		self.assertEqual(Cryon.as_json(self)[answer], False)

# if __name__ == '__main__':
#     unittest.main()