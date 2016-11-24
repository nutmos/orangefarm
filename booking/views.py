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
      booking_id = request.GET.get('booking_id', '')
      booking = Booking.objects.get(id=booking_id)
      pass_data = {
         'name': booking.trip.name,
         'booking_id': booking.id,
         'company_name': booking.company_name,
         'start_date': booking.trip.start_date,
         'end_date': booking.trip.end_date,
         'travel_by': booking.trip.travel_by,
         'remaining_people': booking.trip.remaining_people
      }
      return HttpResponse(template.render(pass_data, request))
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
         booking_id = request.GET.get('booking_id', '')
         booking = Booking.objects.get(id=booking_id)
         adult = request.GET.get('adult', '')
         children = request.GET.get('children', '')
         people = int(adult)+int(children)
         booking.adult = adult
         booking.children = children
         booking.people = people
         booking.save()
         #trip1.remaining_people -= people
         return HttpResponseRedirect('/booking/info?booking_id=' + str(booking.id))
      except:
         return HttpResponse('id is not correct')
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
      booking_id = request.GET.get('booking_id', '')
      booking = Booking.objects.get(id=booking_id)
      p = []
      for i in range(1,int(booking.people)+1): p.append(i)
      pass_data = {
         'booking_id': booking.id,
         'p': p
      }
      return HttpResponse(template.render(pass_data, request))
   except:
      return HttpResponse('id info is not correct')
   return HttpResponse('This page is not complete')

def process_info(request):
   try:
      user_id = request.session['user_id']
      user1 = User.objects.get(id=user_id)
   except:
      template = loader.get_template('login/index.html')
      return HttpResponse(template.render({}, request))
   if request.method == 'GET':
      booking_id = request.GET.get('booking_id', '')
      booking = Booking.objects.get(id=booking_id)
      #for i in range(1,int(booking.people)+1):
         #title = request.GET.get('title', '')
         #print 'title: '+title
         #tourist = Tourist(booking=booking, title=title)
      return HttpResponse('id info is not correct')
   return HttpResponse('This page is not complete')

def checking(request):
   try:
      user_id = request.session['user_id']
      user1 = User.objects.get(id=user_id)
   except:
      template = loader.get_template('login/index.html')
      return HttpResponse(template.render({}, request))
   template = loader.get_template('booking/checking.html')
   try:
      trip_id = request.GET.get('trip_id', '')
      trip1 = Trip.objects.get(id=trip_id)
      company1 = Company.objects.get(id=trip1.company_id)
      adult = request.GET.get('adult', '')
      children = request.GET.get('children', '')
      people = int(adult)+int(children)
      total_price = people*int(trip1.price)
      pass_data = {
         'name': trip1.name,
         'trip_id': trip1.id,
         'company_name': company1.name,
         'start_date': trip1.start_date,
         'end_date': trip1.end_date,
         'travel_by': trip1.travel_by,
         'remaining_people': trip1.remaining_people,
         'price':trip1.price,
         'adult': adult,
         'children': children,
         'total_price': total_price,
         'people': people
      }
      return HttpResponse(template.render(pass_data, request))
   except:
      return HttpResponse(' id is not correct')
   return HttpResponse('This page is not complete')

def payment(request):
   try:
      user_id = request.session['user_id']
      user1 = User.objects.get(id=user_id)
   except:
      template = loader.get_template('login/index.html')
      return HttpResponse(template.render({}, request))
   template = loader.get_template('booking/payment.html')
   try:
      trip_id = request.GET.get('trip_id', '')
      trip1 = Trip.objects.get(id=trip_id)
      company1 = Company.objects.get(id=trip1.company_id)
      adult = request.GET.get('adult', '')
      children = request.GET.get('children', '')
      people = int(adult)+int(children)
      total_price = people*int(trip1.price)
      pass_data = {
         'name': trip1.name,
         'trip_id': trip1.id,
         'company_name': company1.name,
         'remaining_people': trip1.remaining_people,
         'price':trip1.price,
         'adult': adult,
         'children': children,
         'total_price': total_price,
         'people': people
      }
      return HttpResponse(template.render(pass_data, request))
   except:
      return HttpResponse(' id is not correct')
   return HttpResponse('This page is not complete')
