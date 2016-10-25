from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from mongoengine.django.auth import User

# Create your models here.

class User(User):
    email = StringField(max_length=100)
