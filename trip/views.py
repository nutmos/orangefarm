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
from booking.models import *

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
        c1 = Trip(name=name, company_id=company_id, price=price, start_date=start_date, end_date=end_date, max_people=max_people, remaining_people=remaining_people, highlight=highlight, description=description, travel_by=travel_by, conditions=conditions, active=True, company=Company.objects.get(id=company_id))
        c1.save()
        return HttpResponseRedirect('/trip/?trip_id=' + str(c1.id))
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
        except:
            access_edit = False
        try:
            c1 = Trip.objects.get(id=trip_id)
            if c1.active == False:
                return HttpResponse('trip is not available')
            template = loader.get_template('trip/index.html')
            tripplace_list = list(TripPlace.objects.aggregate(
                {'$match': {'trip' : c1.id }},
                    ))
            place_list = [Place.objects.get(id=p['place']) for p in tripplace_list]
            all_photos = list(Place.objects.aggregate(
                    {'$match': {'_id': {'$in': [p['id'] for p in place_list]}}},
                    {'$unwind': '$photos'},
                    {'$project': {'photos': 1, '_id': 0}},
                    {'$sample': {'size': 3}},
                ))
            photo_list = [PlacePicture.objects.get(id=p['photos']) for p in all_photos]
            pass_data = {
                'this_trip': c1,
                'access_edit': access_edit,
                'place_list': place_list,
                'photo_list': photo_list,
                }
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
    tripplace_list = TripPlace.objects(trip=c1)
    place_list = []
    for p in tripplace_list:
        place_list.append(p.place)
    print c1.id
    pass_data = {
        'trip_id': str(c1.id),
        'trip_name': c1.name,
        'place_list': place_list,
        'access_edit': access_edit,
        'nav': '<a href="/trip/?trip_id=' + str(c1.id) + '">' + c1.name + '</a> -> Place',
    }
    return HttpResponse(template.render(pass_data, request))


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
        new_tripplace = TripPlace(trip=c1, place=Place.objects.get(id=place_id))
        new_tripplace.save()
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
        place_list = TripPlace.objects(trip=c1)
        template = loader.get_template('trip/delete-place.html')
        pass_data = {
            'place_list': place_list,
            'name': c1.name,
            'trip_id': trip_id,
            }
        return HttpResponse(template.render(pass_data, request))
    except DoesNotExist:
        return HttpResponse('Cannot find trip')

def process_delete_place(request):
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
        tripplace_id = request.GET.get('tripplace_id', '')
        tripplace = TripPlace.objects.get(id=tripplace_id)
        tripplace.delete()
        return HttpResponseRedirect('/trip/show-place?trip_id=' + str(c1.id))
    return HttpResponse("Error")

def featured_trip(request):
    all_trip = Trip.objects(active=True)
    template = loader.get_template('trip/featured-trip.html')
    pass_data = {
        'trip_list': all_trip,
        'type': 'trip',
        'not_show_header': True,
        }
    return HttpResponse(template.render(pass_data, request))

def process_booking(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
    except:
        template = loader.get_template('login/index.html')
        return HttpResponse(template.render({}, request))
    try:
        trip_id = request.GET.get('trip_id', '')
        trip1 = Trip.objects.get(id=trip_id)
        company1 = Company.objects.get(id=trip1.company_id)
        booking = Booking(trip=trip1, user=user1, company=company1)
        booking.save()
        return HttpResponseRedirect('/booking?booking_id=' + str(booking.id))
    except:
        return HttpResponse("Error")

def show_image(request):
    if request.method == 'GET':
        trip_id = request.GET.get('trip_id', '')
        try:
            c1 = Trip.objects.get(id=trip_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            pass
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))

def handle_change_picture(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id', '')
        c1 = Trip.objects.get(id=trip_id)
        c1.photo.delete()
        image = request.FILES.get('image-upload', '')
        c1.photo.put(image, content_type='image/*')
        c1.save()
        return HttpResponseRedirect('/trip/?trip_id=' + trip_id)
    return HttpResponse("Error")

