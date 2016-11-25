from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from city.models import *
from place.models import *
from user_profile.models import *
from trip.models import *
from django.template import loader
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.


def add_country(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('country/add.html')
    return HttpResponse(template.render({}, request))

def process_add(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        name = request.GET.get('name','')
        url = name.lower().replace(' ', '_').replace('-', '_')
        description = request.GET.get('description','')
        c1 = Country(name=name, description=description, url_point_to=url)
        c1.save()
        return HttpResponseRedirect('/country?country_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        try:
            c1 = Country.objects.get(id=country_id)
            return HttpResponseRedirect('/country/c/' + c1.url_point_to)
        except:
            return HttpResponse('country id is not correct')
    return HttpResponse('This page is not complete')

def country_name(request, country_name):
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
    except:
        access_edit = False
    c1 = Country.objects.get(url_point_to=country_name)
    template = loader.get_template('country/index.html')
    city_list = City.objects(country_id=str(c1.id))
    city_list_id = [str(i.id) for i in city_list]
    place_aggregate = list(Place.objects.aggregate(
        {'$match': {'city_id': {'$in': city_list_id}}},
        {'$sample': {'size': 3}},
        {'$project': {'city': '$city'}},
    ))
    place_list = Place.objects(id__in=[p['_id'] for p in place_aggregate])
    city_aggregate = list(City.objects.aggregate(
        {'$match': {'country_id': str(c1.id)}},
        {'$sample': {'size': 3}},
        {'$project': {'country': '$country'}},
        ))
    city_list = City.objects(id__in=[p['_id'] for p in city_aggregate])
    country_list = list(Country.objects.aggregate(
            {'$sample': {'size': 3}},
        ))
    for c in country_list: c['id'] = c.pop('_id')
    all_place = list(Place.objects.aggregate(
            {'$match': {'city_id': {'$in': city_list_id}}}
            ))
    all_place_id = [a['_id'] for a in all_place]
    tripplace_list = list(TripPlace.objects.aggregate(
            {'$match': {'place': {'$in': all_place_id}}},
            {'$group': {'_id': '$trip'}},
            {'$sample': {'size': 3}},
            ))
    trip_list = [Trip.objects.get(id=a['_id']) for a in tripplace_list]
    pass_data = {
            'this_country': c1,
        'access_edit': access_edit,
        'city_list': city_list,
        'country_list': country_list,
        'place_list': place_list,
        'trip_list': trip_list,
        }
    return HttpResponse(template.render(pass_data, request))

def edit(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        print country_id
        try:
            c1 = Country.objects.get(id=country_id)
            template = loader.get_template('country/edit.html')
            pass_data = {
                'this_country': c1,
                }
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        user_id = request.session['user_id']
        desc = request.GET.get('description', '')
        country_id = request.GET.get('country_id', '')
        c1 = Country.objects.get(id=country_id)
        c1.description = request.GET.get('description', '')
        c1.save()
        pass_data = {'country_id': country_id};
        return HttpResponseRedirect('/country?country_id=' + str(c1.id))
    return HttpResponse('No Request')

def delete(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        try:
            c1 = Country.objects.get(id=country_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

def handle_change_picture(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        country_id = request.POST.get('country_id', '')
        c1 = Country.objects.get(id=country_id)
        c1.photo.delete()
        image = request.FILES.get('image-upload', '')
        c1.photo.put(image, content_type='image/*')
        c1.save()
        return HttpResponseRedirect('/country?country_id=' + country_id)
    return HttpResponse("Error")

def show_image(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        try:
            c1 = Country.objects.get(id=country_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))

def show_city(request, country_name):
    c1 = Country.objects.get(url_point_to=country_name)
    template = loader.get_template('country/city.html')
    place_list = City.objects(country_id=str(c1.id))
    pass_data = {
            'the_place': c1,
            'place_list': place_list,
            'nav': '<a href="/country/?country_id=' + str(c1.id) + '">' + c1.name + '</a> -> City',
        }
    return HttpResponse(template.render(pass_data, request))

def all_country(request):
    c1 = Country.objects.order_by('name')
    template = loader.get_template('country/all-country.html')
    pass_data = {
            'place_list': c1,
            }
    return HttpResponse(template.render(pass_data, request))

def popular_place(request, country_name):
    c1 = Country.objects.get(url_point_to=country_name)
    city_list = City.objects(country_id=str(c1.id))
    city_list_id = [str(i.id) for i in city_list]
    print city_list_id
    place_list = []
    all_place = Place.objects().order_by('name')
    for p in all_place:
        if p.city_id in city_list_id:
            place_list.append(p)
    pass_data = {
            'the_place': c1,
            'place_list': place_list,
            }
    template = loader.get_template('country/popular-place.html')
    return HttpResponse(template.render(pass_data, request))

def featured_trip(request, country_name):
    c1 = Country.objects.get(url_point_to=country_name)
    city_list = City.objects(country_id=str(c1.id))
    place_list = list(Place.objects(city_id__in=[str(a.id) for a in city_list]))
    tripplace_list = list(TripPlace.objects(place__in=place_list).aggregate(
            {'$group': {'_id': '$trip'}}
            ))
    trip_list = [Trip.objects.get(id=a['_id']) for a in tripplace_list]
    pass_data = {
        'trip_list': trip_list,
        'the_place': c1,
        'type': 'country',
        'nav': '<a href="/country/?country_id=' + str(c1.id) + '">' + c1.name + '</a> -> Featured Trip'
    }
    template = loader.get_template('trip/featured-trip.html')
    return HttpResponse(template.render(pass_data, request))
