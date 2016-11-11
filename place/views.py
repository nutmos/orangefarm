from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from country.models import *


# Create your views here.

def add_place(request):
    template = loader.get_template('place/add.html')
    country_list = Country.objects.order_by('name')
    return HttpResponse(template.render({'country_list': country_list}, request))

def process_add(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        city_id = request.GET.get('city-id', '')
        description = request.GET.get('description', '')
        c1 = Place(name=name, city_id=city_id, description=description)
        c1.save()
        return HttpResponseRedirect('/place?place_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            template = loader.get_template('place/index.html')
            pass_data = {
                'name': c1.name,
                'city_id': c1.city_id,
                'description': c1.description,
                'place_id': place_id}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('place id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            template = loader.get_template('place/edit.html')
            pass_data = {
                'name': c1.name,
                'city_id': c1.city_id,
                'description': c1.description,
                'place_id': place_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    if request.method == 'GET':
        #desc = request.GET.get('description', '')
	    #Ecity_id = request.GET.get('city_id', '')
        place_id = request.GET.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        c1.city_id = request.GET.get('city_id', '')
        c1.description = request.GET.get('description', '')
        c1.save()
        pass_data = {'place_id': place_id};
        return HttpResponseRedirect('/place?place_id=' + str(c1.id))
    return HttpResponse('No Request')

def delete(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

def change_picture(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        c1 = Place.objects.get(id=country_id)
        template = loader.get_template('place/change-picture.html')
        return HttpResponse(template.render({'place_id': place_id}, request))
    return HttpResponse("Error")

def handle_change_picture(request):
    if request.method == 'POST':
        place_id = request.POST.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        c1.photo.delete()
        image = request.FILES.get('image-upload', '')
        c1.photo.put(image, content_type='image/*')
        c1.save()
        return HttpResponseRedirect('/place?place_id=' + place_id)
    return HttpResponse("Error")

def show_image(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
