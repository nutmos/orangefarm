from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from models import *
from user_profile.models import *

# Create your views here.

def index(request):
    allow_edit = True
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            allow_edit = False
    except:
        allow_edit = False
    if request.method == 'GET':
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        template = loader.get_template('company_profile/index.html')
        return HttpResponse(template.render({
            'com1': com1,
            'allow_edit': allow_edit,
            }, request))
    return HttpResponse('The page does not complete')

def add(request):
    try:
        user_id = request.session['user_id']
        user1 = User.objects.get(id=user_id)
        if user1.is_staff == False:
            template = loader.get_template('notpermitted.html')
            return HttpResponse(template.render({}, request))
    except:
        template = loader.get_template('notpermitted.html')
        return HttpResponse(template.render({}, request))
    template = loader.get_template('company_profile/add.html')
    return HttpResponse(template.render({}, request))

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
        description = request.GET.get('description', '')
        location = request.GET.get('location', '')
        com1 = Company(name=name, location=location, description=description)
        com1.save()
        return HttpResponseRedirect("/company/?company_id=" + str(com1.id))
    return HttpResponose("Error")

def edit(request):
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
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        template = loader.get_template('company_profile/edit.html')
        pass_data = {
            'name': com1.name,
            'description': com1.description,
            'location': com1.location,
            'company_id': com_id,
        }
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse('The page is not complete')

def process_edit(request):
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
        com_id = request.GET.get('company_id', '')
        com1 = Company.objects.get(id=com_id)
        com1.name = request.GET.get('name', '')
        com1.description = request.GET.get('description', '')
        com1.location = request.GET.get('location', '')
        com1.save()
        return HttpResponseRedirect('/company?company_id=' + str(com_id))
    return HttpResponse('The page is not complete')

def process_add_photo(request):
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
        com_id = request.POST.get('company_id', '')
        photo = request.FILES.get('image-upload','')
        p1 = CompanyPicture()
        p1.photo.put(photo, content_type='image/*')
        p1.save()
        com1 = Company.objects.get(id=com_id)
        com1.photos.append(p1)
        com1.save()
        return HttpResponseRedirect('/company/?company_id=' + com_id)
    return HttpResponse('Not Complete')

def show_image(request):
    if request.method == 'GET':
        try:
            company_picture_id = request.GET.get('company_picture_id', '')
            c1 = CompanyPicture.objects.get(id=company_picture_id)
            binary_img = c1.photo.read()
            if binary_img == None:
                return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
            return HttpResponse(binary_img, 'image/*')
        except:
            try:
                company_id = request.GET.get('company_id', '')
                c1 = Company.objects.get(id=place_id)
                if len (c1.photos) != 0:
                    p1 = c1.photos[0]
                    binary_img = p1.photo.read()
                    if binary_img != None:
                        return HttpResponse(binary_img, 'image/*')
            except:
                pass
    return HttpResponseRedirect(static('pictures/Airplane-Wallpaper.jpg'))
    
