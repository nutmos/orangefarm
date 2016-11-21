from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from datetime import datetime
from place.models import *

# Create your models here.

class TripPlace(Document):
    place = ReferenceField('Place')
    trip = ReferenceField('Trip')

class Trip(Document):
    name = StringField()
    company_id = StringField(max_length=24, min_length=24)
    price = IntField()
    start_date = DateTimeField(default=datetime.now())
    end_date = DateTimeField(default=datetime.now())
    max_people = IntField()
    remaining_people = IntField()
    highlight = StringField()
    description = StringField()
    travel_by = StringField()
    conditions = StringField()
    active = BooleanField()
    placelist = ListField(ReferenceField('TripPlace'))
