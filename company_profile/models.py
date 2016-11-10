from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.
class Photo(Document):
    photo = ImageField()
class Company(Document):
    #email = StringField(max_length=100)
    name = StringField(max_length=100)
    description = StringField(max_length=400)
    location = StringField(max_length=200)
    logo = ImageField()
    photo = ListField(ReferenceField(Photo))
    geolocation = GeoPointField()

