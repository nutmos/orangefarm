from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from datetime import datetime
from company_profile.models import *
from place.models import *

# Create your models here.

class Trip(Document):
    name = StringField()
    company_id = StringField(max_length=24, min_length=24)
    company = ReferenceField('Company')
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

class TripPlace(Document):
    place = ReferenceField('Place', reverse_delete_rule=CASCADE)
    trip = ReferenceField('Trip', reverse_delete_rule=CASCADE)

class Booking(Document):
    trip = ReferenceField('Trip')
    user = ReferenceField('User')
    company_name = StringField()
    book_date = DateTimeField(default=datetime.now())
    people = IntField()
    adult = IntField()
    children = IntField()
