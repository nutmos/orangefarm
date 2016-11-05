from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def index(request):
    template = loader.get_template('city/index.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def add_city(request):
    template = loader.get_template('city/add.html')
    return HttpResponse(template.render({}, request))

def process_add(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')
        country = request.GET.get('country', '')
        description = request.GET.get('description', '')
        c1 = City(name=name, country=country, description=description)
        c1.save()
        return HttpResponseRedirect('/city?city_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            template = loader.get_template('city/index.html')
            pass_data = {
                'name': c1.name,
                'country': c1.country,
                'description': c1.description,
                'city_id': city_id}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('city id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        city_id = request.GET.get('city_id', '')
        print city_id
        try:
            c1 = City.objects.get(id=city_id)
            template = loader.get_template('city/edit.html')
            pass_data = {
                'name': c1.name,
                'country': c1.country,
                'description': c1.description,
                'city_id': city_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
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
    if request.method == 'GET':
        city_id = request.GET.get('city_id', '')
        try:
            c1 = City.objects.get(id=city_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

