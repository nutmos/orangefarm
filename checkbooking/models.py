from __future__ import unicode_literals

from django.db import models
from mongoengine import *
from trip.models import *
from datetime import datetime


class Checkbooking(Document):

	status = StringField()