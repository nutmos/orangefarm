from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from country.models import *
from city.models import *
from place.models import *
from trip.models import *
from mongoengine import *

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    is_login = True
    try:
        a = request.session['user_id']
        request.session.set_expiry(3600)
    except KeyError:
        is_login = False
    country_list = Country._get_collection().aggregate([{
        '$sample': {'size': 6},
        }])['result']
    for c in country_list: c['id'] = c.pop('_id')
    city_list = City._get_collection().aggregate([{
        '$sample': {'size': 6},
        }])['result']
    for c in city_list: c['id'] = c.pop('_id')
    place_list = Place._get_collection().aggregate([{
        '$sample': {'size': 6},
        }])['result']
    for p in place_list: p['id'] = p.pop('_id')
    trip_list = Trip._get_collection().aggregate([{
        '$sample': {'size': 6},
        }])['result']
    for t in trip_list: t['id'] = t.pop('_id')
    pass_data = {
        'country_list': country_list,
        'city_list': city_list,
        'place_list': place_list,
        'trip_list': trip_list,
    }
    return HttpResponse(template.render(pass_data, request))

