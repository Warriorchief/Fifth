from __future__ import unicode_literals
from django.db import models
from datetime import date

class User(models.Model):
    name = models.CharField(max_length = 100)
    alias = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    date_of_birth = models.DateField(default=date.today())
    created_at = models.DateTimeField(auto_now_add = True)

class Poke(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poker")
    to = models.ForeignKey(User, related_name="poked")
    created_at = models.DateTimeField(auto_now_add = True)
