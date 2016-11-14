from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from country.models import *
from django.template import loader
from django.http import JsonResponse
from mongoengine.django.auth import User as MongoUser
from user_profile.models import User

# Create your views here.


def add_city(request):
    user_id = request.session['user_id']
    try:
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
    user_id = request.session['user_id']
    try:
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
        return HttpResponseRedirect('/city?city_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        access_edit = True
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                access_edit = False
                print user1.name
        except:
            access_edit = False
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            template = loader.get_template('city/index.html')
            city_num = City.objects(country_id=c1.country_id).count()
            country1 = Country.objects.get(id=c1.country_id)
            other_city = City.objects(country_id=c1.country_id)
            show_more_city = False
            if len(other_city) > 3:
                import random
                num_list = random.sample(range(len(other_city)), 3)
                print num_list
                other_city = [other_city[num_list[i]] for i in range(3)]
                show_more_city = True
            pass_data = {
                'name': c1.name,
                'country_name': country1.name,
                'description': c1.description,
                'city_id': city_id,
                'other_city': other_city,
                'access_edit': access_edit,
                'show_more_city': show_more_city}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('city id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    user_id = request.session['user_id']
    print user_id
    try:
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        print "except"
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
    user_id = request.session['user_id']
    try:
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
    user_id = request.session['user_id']
    try:
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
    print "get city by country"
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
    user_id = request.session['user_id']
    try:
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
    user_id = request.session['user_id']
    try:
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
