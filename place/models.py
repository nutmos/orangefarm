from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class Photo(Document):
    photo = ImageField()

class Place(Document):
    name = StringField()
    description = StringField()
    city_id = StringField()
    photos = ListField(ReferenceField(Photo))
