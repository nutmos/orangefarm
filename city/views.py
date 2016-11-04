from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def add_city(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        description = request.GET.get('description', '')
        country = request.GET.get('country', '')
        c1 = City(name=name, description=description, country=country)
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
                'description': c1.description,
		'country': c1.country,
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
                'description': c1.description,
		'country' : c1.country,
                'city_id': city_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    if request.method == 'GET':
        desc = request.GET.get('description', '')
	country = request.GET.get('country', '')
        city_id = request.GET.get('city_id', '')
        c1 = City.objects.get(id=city_id)
        c1.description = request.GET.get('description', '')
	c1.country = request.GET.get('country', '')
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

