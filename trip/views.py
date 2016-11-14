from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from country.models import *
from city.models import *
from place.models import *
from user_profile.models import *
from company_profile.models import *
from django.contrib.staticfiles.templatetags.staticfiles import static


# Create your views here.

def add_trip(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('trip/add.html')
    company_list = Company.objects.order_by('name')
    return HttpResponse(template.render({'company_list': company_list}, request))

def process_add(request):
    if request.method == 'GET':
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                template = loader.get_template('notpermitted.html')
                return HttpResponse(template.render({}, request))
        except:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
        name = request.GET.get('name', '')
        company_id = request.GET.get('company_id', '')
        price = request.GET.get('price', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        max_people = request.GET.get('max_people', '')
        remaining_people = request.GET.get('max_people', '')
        highlight = request.GET.get('highlight', '')
        description = request.GET.get('description', '')
        travel_by = request.GET.get('travel_by', '')
        conditions = request.GET.get('conditions', '')
        c1 = Trip(name=name, company_id=company_id, price=price, start_date=start_date, end_date=end_date, max_people=max_people, remaining_people=remaining_people, highlight=highlight, description=description, travel_by=travel_by, conditions=conditions, active=True)
        c1.save()
        return HttpResponseRedirect('/trip?trip_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        trip_id = request.GET.get('trip_id', '')
        access_edit = True
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                access_edit = False
                print user1.name
        except:
            print "except"
            access_edit = False
        try:
            c1 = Trip.objects.get(id=trip_id)
            if c1.active == False:
                return HttpResponse('trip is not available')
            template = loader.get_template('trip/index.html')
            company1 = Company.objects.get(id=c1.company_id)
            pass_data = {
                'name': c1.name,
                'company_id': c1.company_id,
                'company_name': company1.name,
                'price': c1.price,
                'start_date': c1.start_date,
                'end_date': c1.end_date,
                'max_people': c1.description,
                'remaining_people': c1.description,
                'highlight': c1.highlight,
                'description': c1.description,
                'travel_by': c1.travel_by,
                'conditions': c1.conditions,
                'access_edit': access_edit}
            return HttpResponse(template.render(pass_data, request))
        except ValidationError:
            return HttpResponse('trip id is not correct')
    return HttpResponse('This page is not complete')

def edit(request):
    if request.method == 'GET':
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                template = loader.get_template('notpermitted.html')
                return HttpResponse(template.render({}, request))
        except:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
        trip_id = request.GET.get('trip_id', '')
        try:
            c1 = Trip.objects.get(id=trip_id)
            template = loader.get_template('trip/edit.html')
            pass_data = {
                'highlight': c1.highlight,
                'description': c1.description,
                'travel_by': c1.travel_by,
                'conditions': c1.conditions,
                'trip_id': trip_id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_edit(request):
    if request.method == 'GET':
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                template = loader.get_template('notpermitted.html')
                return HttpResponse(template.render({}, request))
        except:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
        trip_id = request.GET.get('trip_id', '')
        c1 = Trip.objects.get(id=trip_id)
        c1.highlight = request.GET.get('highlight', '')
        c1.description = request.GET.get('description', '')
        c1.travel_by = request.GET.get('travel_by', '')
        c1.conditions = request.GET.get('conditions', '')
        c1.save()
        pass_data = {'trip_id': trip_id};
        return HttpResponseRedirect('/trip?trip_id=' + str(c1.id))
    return HttpResponse('No Request')

def delete(request):
    if request.method == 'GET':
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                template = loader.get_template('notpermitted.html')
                return HttpResponse(template.render({}, request))
        except:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
        trip_id = request.GET.get('trip_id', '')
        try:
            c1 = Trip.objects.get(id=trip_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

#def show_image(request):
#    if request.method == 'GET':
#        try:
#            user1 = User.objects.get(id=user_id)
#            if user1.is_staff == False:
#                template = loader.get_template('notpermitted.html')
#                return HttpResponse(template.render({}, request))
#        except:
#            template = loader.get_template('notpermitted.html')
#            return HttpResponse(template.render({}, request))
#        trip_id = request.GET.get('trip_id', '')
#        try:
#            c1 = Trip.objects.get(id=trip_id)
#            binary_img = c1.photo.read()
#            if binary_img == None:
#                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
#            return HttpResponse(binary_img, 'image/*')
#        except:
#            return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
#    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
