from models import *
from django.db import models
from mongoengine import *

def insert_data():
    com1 = Company(
        name="Orange Farm 1",
        description='We are the tour company that many people rely on',
        location='Thailand')
    com1.save()
