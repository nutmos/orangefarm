from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.

class City(Document):
    name = StringField()
    country_id = StringField()
    description = StringField()
    photo = ImageField()
    url_point_to = StringField()
