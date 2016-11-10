from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class Country(Document):
    name = StringField(unique=True, required=True)
    description = StringField()
    photo = ImageField()
    url_point_to = StringField(unique=True, required=True)
