from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from mongoengine.django.auth import User

# Create your models here.

class User(User):
    email = StringField(max_length=100)

#class Users(Document):
#    firstName = StringField(max_length=30)
#    lastName = StringField(max_length=30)
#    middleName = StringField(max_length=30)
#    gender = StringField(max_length=2)
#    dateOfBirth = StringField(max_length=20)
#    password = StringField(max_length=128)
