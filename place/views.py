from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mongoengine import *
from models import *
from django.template import loader
from country.models import *
from city.models import *
from trip.models import *
from user_profile.models import *
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.

def add_place(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('place/add.html')
    country_list = Country.objects.order_by('name')
    return HttpResponse(template.render({'country_list': country_list}, request))

def process_add(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        name = request.GET.get('name', '')
        city_id = request.GET.get('city_id', '')
        description = request.GET.get('description', '')
        city1 = City.objects.get(id=city_id)
        c1 = Place(name=name, city_id=city_id, description=description, city=city1)
        c1.save()
        c1.url_point_to = str(c1.id)[-5:] + '_' + name.lower().replace(' ', '_').replace('-', '_')
        c1.save()
        return HttpResponseRedirect('/place?place_id=' + str(c1.id))
    return HttpResponse('No GET Request')

def index(request):
    if request.method == 'GET':
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            return HttpResponseRedirect("/place/c/" + c1.url_point_to)
        except ValidationError, DoesNotExist:
            return HttpResponse('place id is not correct')
    return HttpResponse('This page is not complete')

def place_name(request, place_name):
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
    except:
        access_edit = False
    try:
        c1 = Place.objects.get(url_point_to=place_name)
        template = loader.get_template('place/index.html')
        city1 = City.objects.get(id=c1.city_id)
        country1 = Country.objects.get(id=city1.country_id)
        #popular_place_list = Place.objects(city_id=str(city1.id))
        popular_place_list = list(Place.objects.aggregate({'$match': {'city_id': str(city1.id)}}, {'$sample': {'size': 3}}))
        for p in popular_place_list : p['id'] = p.pop('_id')
        for p in c1.related:
            try:
                Place.objects.get(id=str(p.id))
            except:
                Place.objects(id=str(c1.id)).update_one(pull__related=p)
        c1 = Place.objects.get(url_point_to=place_name)
        show_related = c1.related
        if len(show_related) > 3:
            import random
            num_list = random.sample(range(len(show_related)), 3)
            show_related = [show_related[num_list[i]] for i in range(3)]
        related_trip = TripPlace.objects(place=c1)
        pass_data = {
            'this_place': c1,
            'host_city': city1,
            'host_country': country1,
            'access_edit': access_edit,
            'place_picture': c1.photos,
            'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> <a href="/city/?city_id=' + str(city1.id) + '">' + city1.name + '</a> -> ' + c1.name,
            'popular_place_list': popular_place_list,
            'background_url': '/place/picture/?place_id=' + str(c1.id),
            'related_place': show_related,
            'related_trip': related_trip,
            }
        return HttpResponse(template.render(pass_data, request))
    except ValidationError, DoesNotExist:
        return HttpResponse('place id is not correct')

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
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            template = loader.get_template('place/edit.html')
            country_list = Country.objects()
            city1 = City.objects.get(id=c1.city_id)
            country1 = Country.objects.get(id=city1.country_id)
            city_list = City.objects(country_id=city1.country_id)
            pass_data = {
                'this_place': c1,
                'host_city': city1,
                'host_country': country1,
                'country_list': country_list,
                'city_list': city_list}
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
        place_id = request.GET.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        new_city_id = request.GET.get('city_id', '')
        if new_city_id != c1.city_id:
            c1.city_id = new_city_id
            del c1.related[:]
            c1.city = City.objects.get(id=new_city_id)
        c1.description = request.GET.get('description', '')
        c1.save()
        return HttpResponseRedirect('/place?place_id=' + str(c1.id))
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
        place_id = request.GET.get('place_id', '')
        try:
            c1 = Place.objects.get(id=place_id)
            c1.delete()
            return HttpResponse('Delete Complete')
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse('No Request GET')

def add_picture(request):
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
        place_id = request.GET.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        if len(c1.photos) >= 4:
            template = loader.get_template('alerttemplate.html')
            return HttpResponse(template.render({
                'header': 'Too Many Image',
                'message': 'Too Many Image',
                'submessage': 'The image is limited to 4 per place.<br>If you want to upload new image, please delete the current one'}, request))
        template = loader.get_template('place/add-picture.html')
        return HttpResponse(template.render({'place_id': place_id}, request))
    return HttpResponse("Error")

def handle_add_picture(request):
    if request.method == 'POST':
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                template = loader.get_template('notpermitted.html')
                return HttpResponse(template.render({}, request))
        except:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
        place_id = request.POST.get('place_id', '')
        c1 = Place.objects.get(id=place_id)
        image = request.FILES.get('image-upload', '')
        p1 = PlacePicture()
        p1.photo.put(image, content_type='image/*')
        p1.save()
        Place.objects(id=place_id).update_one(push__photos=p1)
        return HttpResponseRedirect('/place?place_id=' + place_id)
    return HttpResponse("Error")

def edit_picture(request):
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
        place_id = request.GET.get('place_id', '')
        try:
            p1 = Place.objects.get(id=place_id)
            show_upload = False
            if len(p1.photos) < 4:
                show_upload = True
            template = loader.get_template('place/edit-image.html')
            pass_data = {
                'place_id': place_id,
                'place_picture': p1.photos,
                'name': p1.name,
                'url_point_to': p1.url_point_to,
                'show_upload_button': show_upload,
            }
            return HttpResponse(template.render(pass_data, request))
        except:
            pass
    return HttpResponse("Error")

def handle_delete_picture(request):
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
        picture_id = request.GET.get('picture_id', '')
        place_id = request.GET.get('place_id', '')
        try:
            pic1 = PlacePicture.objects.get(id=picture_id)
            pic1.photo.delete()
            Place.objects(id=place_id).update_one(pull__photos=pic1)
            pic1.delete()
            return HttpResponseRedirect('/place/edit-picture/?place_id=' + place_id)
        except:
            pass
    return HttpResponse("Error")

def show_image(request):
    if request.method == 'GET':
        try:
            place_picture_id = request.GET.get('place_picture_id', '')
            c1 = PlacePicture.objects.get(id=place_picture_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            try:
                place_id = request.GET.get('place_id', '')
                c1 = Place.objects.get(id=place_id)
                if len (c1.photos) != 0:
                    p1 = c1.photos[0]
                    binary_img = p1.photo.read()
                    if binary_img != None:
                        return HttpResponse(binary_img, 'image/*')
            except:
                pass
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))

def show_related(request, place_name):
    access_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            access_edit = False
    except:
        access_edit = False
    template = loader.get_template('place/related.html')
    c1 = Place.objects.get(url_point_to=place_name)
    city1 = City.objects.get(id=c1.city_id)
    country1 = Country.objects.get(id=city1.country_id)
    for p in c1.related:
        try:
            Place.objects.get(id=str(p.id))
        except:
            Place.objects(url_point_to=place_name).update_one(pull__related=p)
    c1 = Place.objects.get(url_point_to=place_name)
    pass_data = {
        'place_list': c1.related,
        'the_place': c1,
        'access_edit': access_edit,
        'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> <a href="/city/?city_id=' + str(city1.id) + '">' + city1.name + '</a> -> <a href="/place/?place_id=' + str(c1.id) + '">' + c1.name + '</a> -> Related',
    }
    return HttpResponse(template.render(pass_data, request))

def delete_related(request, place_name):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    c1 = Place.objects.get(url_point_to=place_name)
    place_list = c1.related
    template = loader.get_template('place/delete-related.html')
    pass_data = {
        'place_list': place_list,
        'name': c1.name,
        'url_point_to': place_name,
        }
    return HttpResponse(template.render(pass_data, request))

def process_delete_related(request, place_name):
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
        c1 = Place.objects.get(url_point_to=place_name)
        del_id = request.GET.get('related_id', '')
        try:
            Place.objects(url_point_to=place_name).update_one(pull__related=Place.objects.get(id=del_id))
            return HttpResponseRedirect("/place/c/" + place_name + "/related/delete")
        except:
            return HttpResponse("Not found")
    return HttpResponse("Error")
        

def add_related(request, place_name):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    c1 = Place.objects.get(url_point_to=place_name)
    place_list = Place.objects(city_id=c1.city_id).order_by('name')
    template = loader.get_template('place/add-related.html')
    pass_data = {
        'place_list': place_list,
        'url_point_to': place_name,
        }
    return HttpResponse(template.render(pass_data, request))

def process_add_related(request, place_name):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    c1 = Place.objects.get(url_point_to=place_name)
    related_place_id = request.GET.get('place-id', '')
    Place.objects(url_point_to=place_name).update_one(push__related=Place.objects.get(id=related_place_id))
    return HttpResponseRedirect('/place/c/'+place_name+'/related/')

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
            pass
    return JsonResponse("Error")

def all_place(request):
    place_list = Place.objects().order_by('name')
    template = loader.get_template('place/all-place.html')
    pass_data = {
        'place_list': place_list,
        }
    return HttpResponse(template.render(pass_data, request))

def featured_trip(request, place_name):
    c1 = Place.objects.get(url_point_to=place_name)
    city1 = City.objects.get(id=c1.city_id)
    country1 = Country.objects.get(id=city1.country_id)
    tripplace_list = TripPlace.objects(place=c1)
    trip_list = [Trip.objects.get(id=a['trip'].id) for a in tripplace_list]
    pass_data = {
        'trip_list': trip_list,
        'the_place': c1,
        'type': 'place',
        'nav': '<a href="/country/?country_id=' + str(country1.id) + '">' + country1.name + '</a> -> <a href="/city/?city_id=' + str(city1.id) + '">' + city1.name + '</a> -> <a href="/place/?place_id=' + str(c1.id) + '">' + c1.name + '</a> -> Featured Trip'
    }
    template = loader.get_template('trip/featured-trip.html')
    return HttpResponse(template.render(pass_data, request))
