from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from user_profile.models import *
from trip.models import *
from datetime import datetime

# Create your models here.

class Tourist(Document):
	title = StringField()
	firstname = StringField()
	lastname = StringField()
	gender = StringField()
	bday = DateTimeField(default=datetime.now())
	nation = StringField()
	citizenid = StringField()
	passportno = StringField()
	mobile = StringField()
	email = StringField()

class Booking(Document):
	trip = ReferenceField('Trip', reverse_delete_rule=CASCADE)
	user = ReferenceField('User', reverse_delete_rule=CASCADE)
	company_name = StringField()
	book_date = DateTimeField(default=datetime.now())
	people = IntField()
	adult = IntField()
	children = IntField()
	member = ListField(ReferenceField('Tourist'))
	total_price = IntField()
	status = BooleanField(default='False')
	confirm = BooleanField(default='False')
