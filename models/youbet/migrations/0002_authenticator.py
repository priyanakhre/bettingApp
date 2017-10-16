# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-12 04:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youbet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('authenticator', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('date_created', models.DateField(blank=True, default=datetime.datetime.now)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='youbet.User')),
            ],
        ),
    ]
