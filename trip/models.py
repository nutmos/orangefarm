from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class Trip(Document):
    name = StringField()
    company_id = StringField()
    price = IntField()
    start_date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField(default=datetime.datetime.now)
    max_people = IntField()
    remaining_people = IntField()
    highlight = StringField()
    description = StringField()
    travel_by = StringField()
    conditions = StringField()
    active = BooleanField()