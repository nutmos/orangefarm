from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from country.models import *
from place.models import *
from django.template import loader
from django.http import JsonResponse
from mongoengine.django.auth import User as MongoUser
from user_profile.models import User

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
        country_id = request.GET.get('country-id', '')
        try:
            co1 = Country.objects.get(id=country_id)
        except:
            return HttpResponseRedirect('/city/add')
        description = request.GET.get('description', '')
        c1 = City(name=name, country_id=country_id, description=description)
        c1.save()
        c1.url_point_to = str(c1.id)[-5:] + '_' + name.lower().replace(' ', '_')
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
        other_city = City._get_collection().aggregate([{
            '$sample': {'size': 3}
            }])['result']
        for c in other_city: c['id'] = c.pop('_id')
        popular_place = Place._get_collection().aggregate([{
            '$sample': {'size': 3}
            }])['result']
        for p in popular_place: p['id'] = p.pop('_id')
        pass_data = {
            'this_city': c1,
            'host_country': country1,
            'other_city': other_city,
            'access_edit': access_edit,
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
            return HttpResponse('1city id is not correct')
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
            print country_list
            pass_data = {
                'name': c1.name,
                'selected_country_name': c1country.name,
                'description': c1.description,
                'city_id': city_id,
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
        #desc = request.GET.get('description', '')
	    #Ecountry = request.GET.get('country', '')
        city_id = request.GET.get('city_id', '')
        c1 = City.objects.get(id=city_id)
        c1.country = request.GET.get('country', '')
        c1.description = request.GET.get('description', '')
        c1.save()
        pass_data = {'city_id': city_id};
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
            print c_json
            return JsonResponse(c_json)
        except:
            print "except"
            pass
    return HttpResponse("Error")

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
def change_picture(request):
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
        template = loader.get_template('city/change-picture.html')
        return HttpResponse(template.render({'city_id': city_id}, request))
    return HttpResponse("Error")

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
