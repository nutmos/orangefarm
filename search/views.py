from django.shortcuts import render
from login.models import *
from django.http import HttpResponse
from django.template import loader
import urllib
from country.models import *
from city.models import *
from place.models import *
from company_profile.models import *

# Create your views here.

def index(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        query_unquote =  urllib.unquote(query)
        country_list = Country.objects(__raw__={'name': {'$regex': query_unquote, '$options': 'i' }})
        place_list = Place.objects(__raw__={'name': {'$regex': query_unquote, '$options': 'i' }})
        city_list = City.objects(__raw__={'name': {'$regex': query_unquote, '$options': 'i' }})
        company_list = Company.objects(__raw__={'name': {'$regex': query_unquote, '$options': 'i'}})
        pass_data = {
            'query': query_unquote,
            'country_list': country_list,
            'city_list': city_list,
            'place_list': place_list,
            'company_list': company_list,
        }
        template = loader.get_template('search/index.html')
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse("Not Complete")
