from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from user_profile.models import *
from datetime import datetime

# Create your models here.
class CompanyPicture(Document):
    photo = ImageField()
class Company(Document):
    #email = StringField(max_length=100)
    name = StringField(max_length=100)
    description = StringField()
    location = StringField(max_length=200)
    logo = ImageField()
    photos = ListField(ReferenceField('CompanyPicture'))
class ReviewCompany(Document):
    rating = IntField(min_value=1, max_value=5)
    comment = StringField()
    user = ReferenceField('User')
    company = ReferenceField('Company', reverse_delete_rule=CASCADE)
    timestamp = DateTimeField(default=datetime.now())
