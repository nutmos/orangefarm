from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from trip.models import *
from datetime import datetime


class Checkbooking(Document):
	user_id = StringField()
	trip_id = StringField()
	book_date = DateTimeField(default=datetime.now())
	people = IntField()
	status = StringField()