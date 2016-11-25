from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mongoengine import *
from models import *
from country.models import *
from place.models import *
from trip.models import *
from django.template import loader
from mongoengine.django.auth import User as MongoUser
from user_profile.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.


def add_city(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('city/add.html')
    country_list = Country.objects.order_by('name')
    return HttpResponse(template.render({'country_list': country_list}, request))

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
        name = request.GET.get('name', '')
        country_id = request.GET.get('country_id', '')
        country1 = None
        try:
            co1 = Country.objects.get(id=country_id)
            country1 = co1
        except:
            return HttpResponseRedirect('/city/add')
        description = request.GET.get('description', '')
        c1 = City(name=name, country_id=country_id, description=description, country=country1)
        c1.save()
        c1.url_point_to = str(c1.id)[-5:] + '_' + name.lower().replace(' ', '_').replace('-', '_')
        c1.save()
        return HttpResponseRedirect('/city?city_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def city_name(request,city_name):
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
    except:
        access_edit = False
    try:
        c1 = City.objects.get(url_point_to=city_name)
        template = loader.get_template('city/index.html')
        country1 = Country.objects.get(id=c1.country_id)
        other_city_aggregate = list(City.objects.aggregate(
            {'$match': {'country': country1.id, '_id': {'$ne': c1.id}}},
            {'$sample': {'size': 3}},
            {'$project': {'country': 1}},
            ))
        other_city = City.objects(id__in=[a['_id'] for a in other_city_aggregate])
        popular_place_agg = list(Place.objects.aggregate(
            {'$match': {'city': c1.id}},
            {'$sample': {'size': 3}},
            {'$project': {'city': 1}},
            ))
        popular_place = Place.objects(id__in=[a['_id'] for a in popular_place_agg])
        all_place = Place.objects(city=c1)
        all_place_id = [a.id for a in all_place]
        tripplace_list = list(TripPlace.objects.aggregate(
            {'$match': {'place': {'$in': all_place_id}}},
            {'$group': {'_id': '$trip'}},
            {'$sample': {'size': 3}},
            ))
        trip_list = [Trip.objects.get(id=a['_id']) for a in tripplace_list]
        pass_data = {
            'this_city': c1,
            'host_country': country1,
            'other_city': other_city,
            'access_edit': access_edit,
            'trip_list': trip_list,
            'popular_place': popular_place,
            'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> ' + c1.name,
            }
        return HttpResponse(template.render(pass_data, request))
    except:
        return HttpResponse('city id is not correct')

def index(request):
    if request.method == 'GET':
        try:
            city_id = request.GET.get('city_id', '')
            c1 = City.objects.get(id=city_id)
            return HttpResponseRedirect('/city/c/'+c1.url_point_to)
        except:
            return HttpResponse('city id is not correct')
    return HttpResponse('This page is not complete')

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
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            template = loader.get_template('city/edit.html')
            country_list = Country.objects.order_by('name')
            c1country = Country.objects.get(id=c1.country_id)
            pass_data = {
                'this_city': c1,
                'host_country': c1country,
                'country_list': country_list}
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
        city_id = request.GET.get('city_id', '')
        c1 = City.objects.get(id=city_id)
        if (c1.id == ''):
            return HttpResponseRedirect('/city/edit/?city_id=' + city_id)
        country_id = request.GET.get('country_id', '')
        c1.country_id = country_id
        c1.country = Country.objects.get(id=country_id)
        c1.description = request.GET.get('description', '')
        c1.save()
        return HttpResponseRedirect('/city?city_id=' + str(c1.id))
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
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

def get_city_by_country(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        try:
            c1 = City.objects(country_id=country_id).order_by('name')
            c_json = {}
            for c in c1:
                c_json[c.name] = str(c.id)
            return JsonResponse(c_json)
        except:
            pass
    return JsonResponse("Error")

def show_image(request):
    if request.method == 'GET':
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))

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
        city_id = request.POST.get('city_id', '')
        c1 = City.objects.get(id=city_id)
        c1.photo.delete()
        image = request.FILES.get('image-upload', '')
        c1.photo.put(image, content_type='image/*')
        c1.save()
        return HttpResponseRedirect('/city?city_id=' + city_id)
    return HttpResponse("Error")

def popular_place(request, city_name):
    c1 = City.objects.get(url_point_to=city_name)
    place_list = Place.objects(city_id=str(c1.id)).order_by('-rating', 'name')
    country1 = Country.objects.get(id=c1.country_id)
    template = loader.get_template("city/popular-place.html")
    pass_data = {
            'the_place': c1,
            'place_list': place_list,
            'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> <a href="/city/?city_id=' + str(c1.id) + '">' +c1.name + '</a> -> Popular', 
            }
    return HttpResponse(template.render(pass_data, request))

def all_city(request):
    c1 = City.objects()
    template = loader.get_template("city/all-city.html")
    pass_data = {
        'place_list': c1,
        }
    return HttpResponse(template.render(pass_data, request))

def featured_trip(request, city_name):
    c1 = City.objects.get(url_point_to=city_name)
    country1 = Country.objects.get(id=c1.country_id)
    place_list = list(Place.objects(city_id=str(c1.id)))
    tripplace_list = list(TripPlace.objects(place__in=place_list).aggregate(
            {'$group': {'_id': '$trip'}}
            ))
    trip_list = [Trip.objects.get(id=a['_id']) for a in tripplace_list]
    pass_data = {
        'trip_list': trip_list,
        'the_place': c1,
        'type': 'city',
        'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> <a href="/city/?city_id=' + str(c1.id) + '">' + c1.name + '</a> -> Featured Trip'
    }
    template = loader.get_template('trip/featured-trip.html')
    return HttpResponse(template.render(pass_data, request))
