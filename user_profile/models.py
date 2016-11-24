from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from mongoengine.django.auth import User as MongoUser
from trip.models import *

# Create your models here.

class User(MongoUser):
    #email = StringField(max_length=100)
    bio = StringField(max_length=200)
    photo = ImageField()
    name = StringField(max_length=100)
    #history
    trip_id = StringField()
    