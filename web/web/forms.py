from django import forms
import datetime

class RegisterForm(forms.Form):
	first_name = forms.CharField(label='First name', max_length=100)
	last_name = forms.CharField(label='Last name', max_length=100)
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=30)
	confirm_password = forms.CharField(label='Confirm Password', max_length=30)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=30)


class CreateBetForm(forms.Form):
	privacy = forms.BooleanField(label='Private?')
	response_limit = forms.IntegerField(label='Response Limit')
	category = forms.CharField(label='Category',max_length=50)
	question = forms.CharField(label='Question', max_length=200)
	description = forms.CharField(label="Description", max_length=500)
	min_buyin = forms.IntegerField(label="Minimum Buy-In")
	per_person_cap = forms.IntegerField(label="Per Person Cap")
	expiration = forms.DateTimeField(label = "Expiration")