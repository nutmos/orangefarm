from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from country.models import *

# Create your models here.

class City(Document):
    name = StringField()
    country_id = StringField()
    country = ReferenceField('Country', reverse_delete_rule=CASCADE)
    description = StringField()
    photo = ImageField()
    url_point_to = StringField(unique=True)
