from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class Place(Document):
    name = StringField()
    description = StringField()
    city_id = StringField()
