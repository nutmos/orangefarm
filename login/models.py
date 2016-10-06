from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class User(Document):
    username = StringField(max_length=30)
    password = StringField(max_length=128)
    def addData(user, pas):
        username = user
        passsword = pas
