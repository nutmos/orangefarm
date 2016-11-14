from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from city.models import *
from user_profile.models import *
from django.template import loader
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.


def add_country(request):
    user_id = request.session['user_id']
    try:
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
        name = request.GET.get('name','')
        url = name.lower().replace(' ', '_')
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
        except ValidationError:
            return HttpResponse('country id is not correct')
    return HttpResponse('This page is not complete')

def country_name(request, country_name):
    print "country_name = " + country_name
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
            print user1.name
    except:
        access_edit = False
    c1 = Country.objects.get(url_point_to=country_name)
    template = loader.get_template('country/index.html')
    city_list = City.objects(country_id=str(c1.id))
    pass_data = {
        'name': c1.name, 
        'description': c1.description,
        'country_id': str(c1.id),
        'access_edit': access_edit,
        'city_list': city_list[:3]}
    return HttpResponse(template.render(pass_data, request))

def edit(request):
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
        country_id = request.GET.get('country_id', '')
        print country_id
        try:
            c1 = Country.objects.get(id=country_id)
            template = loader.get_template('country/edit.html')
            pass_data = {
                'name': c1.name,
                'description': c1.description,
                'country_id': country_id}
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
        country_id = request.GET.get('country_id', '')
        try:
            c1 = Country.objects.get(id=country_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

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
        country_id = request.GET.get('country_id', '')
        c1 = Country.objects.get(id=country_id)
        template = loader.get_template('country/change-picture.html')
        return HttpResponse(template.render({'country_id': country_id}, request))
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
