from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from django.contrib.staticfiles.templatetags.staticfiles import static
from user_profile.models import *
from booking.models import *

# Create your views here.

def index(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('checkbooking/index.html')
    booking = Booking.objects(confirm=True)
    #booking = Booking.objects()
    book = []
    for o in booking:
        book.append(o)
    pass_data = {
        'book': book
        }
    return HttpResponse(template.render(pass_data, request))

def process_confirm(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    booking_id = request.GET.get('booking_id', '')
    booking = Booking.objects.get(id=booking_id)
    booking.status = True
    booking.save()
    return HttpResponseRedirect('/checkbooking')