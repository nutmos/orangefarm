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
    return HttpResponseRedirect('/')

def index(request):
    return HttpResponse('This page is not complete')
