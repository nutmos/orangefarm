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
         booking.status = False
         booking.confirm = False
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
         'name': booking.trip.name,
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
      print booking_id
      booking = Booking.objects.get(id=booking_id)
      for x in booking.member:
         Booking.objects(id=booking_id).update_one(pull__member=x)
         x.delete()
      for i in range(1,int(booking.people)+1):
         title = request.GET.get('title-'+str(i), '')
         firstname = request.GET.get('firstname-'+str(i), '')
         lastname = request.GET.get('lastname-'+str(i), '')
         gender = request.GET.get('gender-'+str(i), '')
         bday_str = request.GET.get('bday-' + str(i) ,'')
         bday = datetime.strptime(bday_str, '%Y-%m-%d')
         nation = request.GET.get('nation-'+str(i), '')
         citizenid = request.GET.get('citizenid-'+str(i), '')
         passportno = request.GET.get('passportno-'+str(i),'')
         mobile = request.GET.get('mobile-'+str(i), '')
         email = request.GET.get('email-'+str(i), '')
         print title, firstname, lastname, gender
         tourist = Tourist(title=title, firstname=firstname, lastname=lastname, gender=gender, bday=bday, nation=nation, citizenid=citizenid, passportno=passportno, mobile=mobile, email=email)
         tourist.save()
         Booking.objects(id=booking_id).update_one(push__member=tourist)
      return HttpResponseRedirect('/booking/checking?booking_id=' + str(booking.id))
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
      booking_id = request.GET.get('booking_id', '')
      booking = Booking.objects.get(id=booking_id)
      trip1 = booking.trip
      company1 = trip1.company
      people = int(booking.people)
      total_price = people * int(trip1.price)
      booking.total_price = total_price
      booking.save()
      pass_data = {
        'this_booking': booking,
        'total_price': total_price,
      }
      return HttpResponse(template.render(pass_data, request))
   except:
      return HttpResponse('id is not correct')
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
      booking_id = request.GET.get('booking_id', '')
      booking = Booking.objects.get(id=booking_id)
      trip1 = booking.trip
      company1 = Company.objects.get(id=trip1.company_id)
      people = booking.people
      total_price = booking.total_price
      pass_data = {
         'booking_id': booking.id,
         'name': trip1.name,
         'company_name': company1.name,
         'remaining_people': trip1.remaining_people,
         'total_price': total_price,
         'people': people
      }
      return HttpResponse(template.render(pass_data, request))
   except:
      return HttpResponse(' id is not correct')
   return HttpResponse('This page is not complete')

def process_payment(request):
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
            trip1 = booking.trip
            people = booking.people
            trip1.remaining_people -= people
            trip1.save()
            booking.confirm = True
            booking.save()
            return HttpResponseRedirect('/booking/finish?booking_id=' + str(booking.id))
         except:
            return HttpResponse('id is not correct')
      return HttpResponse('no')

def finish(request):
   template = loader.get_template('booking/finish.html')
   return HttpResponse(template.render({'foo': 'bar'}, request))
