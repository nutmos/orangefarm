from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('place/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def add_place(request):
    template = loader.get_template('place/add.html')
    return HttpResponse(template.render({}, request))

def process_add(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        city = request.GET.get('city', '')
        description = request.GET.get('description', '')
        c1 = Place(name=name, city=city, description=description)
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
                'city': c1.city,
                'description': c1.description,
                'place_id': place_id}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('place id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        print place_id
        try:
            c1 = Place.objects.get(id=place_id)
            template = loader.get_template('place/edit.html')
            pass_data = {
                'name': c1.name,
                'city': c1.city,
                'description': c1.description,
                'place_id': place_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    if request.method == 'GET':
        #desc = request.GET.get('description', '')
	    #Ecity = request.GET.get('city', '')
        place_id = request.GET.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        c1.city = request.GET.get('city', '')
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

