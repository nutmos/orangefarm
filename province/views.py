from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def add_province(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        description = request.GET.get('description', '')
        country = request.GET.get('country', '')
        c1 = Province(name=name, description=description, country=country)
	c1.save()
	return HttpResponseRedirect('/province?province_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        country_id = request.GET.get('province_id', '')
        try:
            c1 = Province.objects.get(id=province_id)
            template = loader.get_template('province/index.html')
            pass_data = {
                'name': c1.name,
                'description': c1.description,
		'country': c1.country,
                'province_id': province_id}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('province id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        province_id = request.GET.get('province_id', '')
        print province_id
        try:
            c1 = Province.objects.get(id=province_id)
            template = loader.get_template('province/edit.html')
            pass_data = {
                'name': c1.name,
                'description': c1.description,
		'country' : c1.country,
                'country_id': country_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

