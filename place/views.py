from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mongoengine import *
from models import *
from django.template import loader
from country.models import *
from city.models import *
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
        city_id = request.GET.get('city-id', '')
        description = request.GET.get('description', '')
        c1 = Place(name=name, city_id=city_id, description=description)
        c1.save()
        c1.url_point_to = str(c1.id)[-5:] + '_' + name.lower().replace(' ', '_')
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
            print user1.name
    except:
        access_edit = False
    try:
        c1 = Place.objects.get(url_point_to=place_name)
        template = loader.get_template('place/index.html')
        city1 = City.objects.get(id=c1.city_id)
        popular_place_list = Place.objects(city_id=str(city1.id))
        pass_data = {
            'name': c1.name,
            'city_id': c1.city_id,
            'city_name': city1.name,
            'description': c1.description,
            'place_id': str(c1.id),
            'access_edit': access_edit,
            'place_picture': c1.photos,
            'popular_place_list': popular_place_list}
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
            country_id = Country.objects.get(id=city1.country_id)
            city_list = City.objects(country_id=city1.country_id)
            pass_data = {
                'name': c1.name,
                'city_id': c1.city_id,
                'description': c1.description,
                'place_id': place_id,
                'country_list': country_list,
                'country_id': country_id,
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
        c1.city_id = request.GET.get('city_id', '')
        c1.description = request.GET.get('description', '')
        c1.save()
        pass_data = {'place_id': place_id};
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
            return HttpResponse("This place has too many image. Please remove before add the new one.")
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
        c1.photos.append(p1)
        c1.save()
        return HttpResponseRedirect('/place?place_id=' + place_id)
    return HttpResponse("Error")

def delete_picture(request):
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
            template = loader.get_template('place/delete-image.html')
            print "test1"
            pass_data = {
                'place_id': place_id,
                'place_picture': p1.photos
            }
            return HttpResponse(template.render(pass_data, request))
        except:
            print "except"
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
            p1 = Place.objects.get(id=place_id)
            pic1 = PlacePicture.objects.get(id=picture_id)
            for i in range(len(p1.photos)):
                if p1.photos[i].id == pic1.id:
                    del p1.photos[i]
            pic1.delete()
            p1.save()
            return HttpResponse("Success")
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

def get_place_by_city(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id', '')
        try:
            c1 = City.objects(country_id=country_id).order_by('name')
            c_json = {}
            for c in c1:
                c_json[c.name] = str(c.id)
            print c_json
            return JsonResponse(c_json)
        except:
            print "except"
            pass
    return HttpResponse("Error")
