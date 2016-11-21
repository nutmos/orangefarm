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
from django.http import JsonResponse


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
        start_date_str = request.GET.get('start_date', '')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date_str = request.GET.get('end_date', '')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
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
                'max_people': c1.max_people,
                'remaining_people': c1.remaining_people,
                'highlight': c1.highlight,
                'description': c1.description,
                'travel_by': c1.travel_by,
                'conditions': c1.conditions,
                'access_edit': access_edit,
                'trip_id': str(c1.id)}
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
                'trip_id': c1.id}
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

def show_place(request):
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
    except:
        access_edit = False
    template = loader.get_template('trip/show-place.html')
    trip_id = request.GET.get('trip_id', '')
    c1 = Trip.objects.get(id=trip_id)
    pass_data = {
        'trip_id': c1.id,
        'trip_name': c1.name,
        'place_list': c1.placelist,
        'access_edit': access_edit,
    }
    return HttpResponse(template.render(pass_data, request))

def get_place_by_city(request):
    if request.method == 'GET':
        city_id = request.GET.get('city_id', '')
        try:
            c1 = Place.objects(city_id=city_id).order_by('name')
            c_json = {}
            for c in c1:
                c_json[c.name] = str(c.id)
            print c_json
            return JsonResponse(c_json)
        except:
            print "in except"
            pass
    return HttpResponse("Error")

def add_place(request):
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
            template = loader.get_template('trip/add-place.html')
            country_list = Country.objects.order_by('name')
            pass_data = {
                'country_list': country_list,
                'name': c1.name,
                'trip_id': c1.id}
            return HttpResponse(template.render(pass_data, request))
        except DoesNotExist:
            return HttpResponse('Key error')
    return HttpResponse('No request')

def process_add_place(request):
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
        trip_id = request.GET.get('trip-id', '')
        c1 = Trip.objects.get(id=trip_id)
        place_id = request.GET.get('place-id', '')
        c1.conditions = request.GET.get('conditions', '')
        c1.placelist.append(Place.objects.get(id=place_id))
        c1.save()
        return HttpResponseRedirect('/trip/show-place?trip_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def delete_place(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    try:
        trip_id = request.GET.get('trip_id', '')
        c1 = Trip.objects.get(id=trip_id)
        place_list = c1.placelist
        template = loader.get_template('trip/delete-place.html')
        pass_data = {
            'place_list': place_list,
            'name': c1.name,
            'trip_id': c1.id}
        return HttpResponse(template.render(pass_data, request))
    except DoesNotExist:
        return HttpResponse('Key error')

def process_delete_place(request):
    print "in"
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
        trip_id = request.GET.get('trip_id','')
        c1 = Trip.objects.get(id=trip_id)
        del_id = request.GET.get('place_id', '')
        for i in range(len(c1.placelist)):
            if str(c1.placelist[i].id) == del_id:
                del c1.placelist[i]
                c1.save()
                return HttpResponseRedirect('/trip/show-place?trip_id=' + str(c1.id))
        return HttpResponse("Not found")
    return HttpResponse("Error")
