from django.db import models
from datetime import datetime

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    num_tokens = models.IntegerField()
    num_flags = models.IntegerField()
    joined_date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.username

    def as_json(self):
        return dict(
            id = self.id,
            first_name = self.first_name,
            last_name = self.last_name,
            username = self.username,
            password = self.password,
            num_tokens = self.num_tokens,
            num_flags = self.num_flags
        )


class Bet(models.Model):
    privacy = models.BooleanField()
    response_limit = models.IntegerField()
    category = models.CharField(max_length=50, default='misc')
    question = models.CharField(max_length=200)
    description = models.TextField()
    outcome = models.NullBooleanField(blank=True, null=True)
    min_buyin = models.IntegerField()
    per_person_cap = models.IntegerField()
    initiation = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)

    def as_json(self):
        return dict(
            id = self.id,
            privacy = self.privacy,
            response_limit = self.response_limit,
            category = self.category,
            question = self.question,
            description = self.description,
            outcome = self.outcome,
            min_buyin = self.min_buyin,
            per_person_cap = self.per_person_cap,
            initiation = self.initiation,
            expiration = self.expiration
        )

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, blank=True, null=True)
    answer = models.BooleanField()
    amount = models.IntegerField()
    resp_timestamp = models.DateTimeField(default=datetime.now, blank=True)

    def as_json(self):
        return dict(
            id=self.id,
            user=User.as_json(self.user),
            bet=Bet.as_json(self.bet),
            answer=self.answer,
            amount=self.amount,
            resp_timestamp=self.resp_timestamp
        )
