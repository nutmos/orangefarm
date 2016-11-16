from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class PlacePicture(Document):
    photo = ImageField()

class Place(Document):
    name = StringField()
    description = StringField()
    city_id = StringField()
    photos = ListField(ReferenceField('PlacePicture'))
    related = ListField(ReferenceField('self'))
    url_point_to = StringField()
