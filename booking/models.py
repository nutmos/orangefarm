from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from user_profile.models import *
from trip.models import *
from datetime import datetime

# Create your models here.

class Booking(Document):
	trip = ReferenceField('Trip', reverse_delete_rule=CASCADE)
	user = ReferenceField('User', reverse_delete_rule=CASCADE)
	company_name = StringField()
	book_date = DateTimeField(default=datetime.now())
	people = IntField()
	adult = IntField()
	children = IntField()
		
class Tourist(Document):
	booking = ReferenceField('Booking', reverse_delete_rule=CASCADE)
	title = StringField()
	firstname = StringField()
	lastname = StringField()
