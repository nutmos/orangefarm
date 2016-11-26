from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from city.models import *
from user_profile.models import *
from datetime import datetime

# Create your models here.

class PlacePicture(Document):
    photo = ImageField()

class Place(Document):
    name = StringField()
    description = StringField()
    city_id = StringField()
    city = ReferenceField('City', reverse_delete_rule=CASCADE)
    photos = ListField(ReferenceField('PlacePicture'))
    related = ListField(ReferenceField('self'))
    url_point_to = StringField(unique=True)

class ReviewPlace(Document):
    rating = IntField(min_value=1, max_value=5)
    comment = StringField()
    user = ReferenceField('User')
    place = ReferenceField('Place', reverse_delete_rule=CASCADE)
    timestamp = DateTimeField(default=datetime.now())
