from django.test import TestCase
from models import Company

# Create your tests here.

class CompanyTest(TestCase):
    def setup(self):
        com1 = Company(
               name="Orange Farm 1",
               description='We are the tour company that many people rely on',
               location='Thailand')
        com1.save()
