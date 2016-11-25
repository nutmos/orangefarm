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
    country_list = list(Country.objects.aggregate(
            {'$sample': {'size': 6}}
        ))
    for c in country_list: c['id'] = c.pop('_id')
    city_aggregate = list(City.objects.aggregate(
        {'$sample': {'size': 6}},
        {'$project': {'country': '$country'}}
        ))
    city_list = City.objects(id__in=[a['_id'] for a in city_aggregate])
    place_aggregate = list(Place.objects.aggregate({
        '$sample': {'size': 6},
        }))
    place_list = Place.objects(id__in=[a['_id'] for a in place_aggregate])
    trip_list = list(Trip.objects.aggregate({
        '$sample': {'size': 6},
        }))
    for t in trip_list: t['id'] = t.pop('_id')
    pass_data = {
        'country_list': country_list,
        'city_list': city_list,
        'place_list': place_list,
        'trip_list': trip_list,
    }
    return HttpResponse(template.render(pass_data, request))

