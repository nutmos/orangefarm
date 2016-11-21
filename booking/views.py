from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from trip.models import *
from company_profile.models import *
from user_profile.models import *

# Create your views here.

def index(request):
	try:
		user_id = request.session['user_id']
		user1 = User.objects.get(id=user_id)
	except:
		template = loader.get_template('login/index.html')
		return HttpResponse(template.render({}, request))
	template = loader.get_template('booking/index.html')
   	try:
   		trip_id = request.GET.get('trip_id', '')
   		trip1 = Trip.objects.get(id=trip_id)
   		company1 = Company.objects.get(id=trip1.company_id)
   		return HttpResponse(template.render({'name': trip1.name, 'trip_id': trip1.id, 'company_name': company1.name, 'start_date': trip1.start_date, 'end_date': trip1.end_date, 'travel_by': trip1.travel_by, 'remaining_people': trip1.remaining_people}, request))
   	except:
   		return HttpResponse(' id is not correct')
   	return HttpResponse('This page is not complete')
    
def process_index(request):
   try:
      user_id = request.session['user_id']
      user1 = User.objects.get(id=user_id)
   except:
      template = loader.get_template('login/index.html')
      return HttpResponse(template.render({}, request))
   if request.method == 'GET':
      try:
         trip_id = request.GET.get('trip_id', '')
         trip1 = Trip.objects.get(id=trip_id)
         return HttpResponseRedirect('/booking/info?trip_id=' + str(trip1.id))
      except:
         return HttpResponse(' id is not correct')
   return HttpResponse('no')


def info(request):
   try:
      user_id = request.session['user_id']
      user1 = User.objects.get(id=user_id)
   except:
      template = loader.get_template('login/index.html')
      return HttpResponse(template.render({}, request))
   template = loader.get_template('booking/info.html')
   try:
      trip_id = request.GET.get('trip_id', '')
      trip1 = Trip.objects.get(id=trip_id)
      return HttpResponse(template.render({'name': trip1.name, 'trip_id': str(trip1.id)}, request))
   except:
      return HttpResponse(' id is not correct')
   return HttpResponse('This page is not complete')

def checking(request):
	template = loader.get_template('booking/checking.html')
	try:
   		trip_id = request.GET.get('trip_id', '')
   		trip1 = Trip.objects.get(id=trip_id)
   		return HttpResponse(template.render({'name': trip1.name, 'trip_id': str(trip1.id)}, request))
   	except:
   		return HttpResponse(' id is not correct')
   	return HttpResponse('This page is not complete')

def payment(request):
    template = loader.get_template('booking/payment.html')
    return HttpResponse(template.render({'foo': 'bar'}, request))
