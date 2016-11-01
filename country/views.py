from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader


# Create your views here.

def add_country(request):
    if request.method == 'GET':
        name = request.GET.get('name','')
        description = request.GET.get('description', '')
        c1 = Country(name=name, description=description)
        c1.save()
    return HttpResponseRedirect('/')

def index(request):
    return HttpResponse('This page is not complete')
