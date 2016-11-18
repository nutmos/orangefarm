from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from trip.models import *

# Create your views here.

def index(request):
   template = loader.get_template('booking/index.html')
   try:
   	trip_id = request.GET.get('trip_id', '')
   	trip1 = Trip.objects.get(id=trip_id)
   	return HttpResponse(template.render({'name': trip1.name, 'id': str(trip1.id)}, request))
   except:
    return HttpResponse(' id is not correct')
   return HttpResponse('This page is not complete')
    

def info(request):
    template = loader.get_template('booking/info.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def checking(request):
    template = loader.get_template('booking/checking.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))

def payment(request):
    template = loader.get_template('booking/payment.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))
