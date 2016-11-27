from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.staticfiles.templatetags.staticfiles import static
from models import *
from user_profile.models import *
from trip.models import *
from booking.models import *

# Create your views here.

def index(request):
    try:
        access_edit = True
        user_id=''
        try:
            user_id = request.session['user_id']
            user1 = User.objects.get(id=user_id)
            if user1.is_staff == False:
                access_edit = False
        except:
            access_edit = False
        if request.method == 'GET':
            com_id = request.GET.get('company_id', '')
            com1 = Company.objects.get(id=com_id)
            com_trip = Trip.objects(company=com1, active=True).limit(3)
            template = loader.get_template('company_profile/index.html')
            review = ReviewCompany.objects(company=com1)
            allow_review = False
            allow_delete_review = []
            try:
                user1 = User.objects.get(id=user_id)
                for i in range(len(review)):
                    if review[i].user.id == user1.id:
                        allow_delete_review.append(i)
                if Booking.objects(company=com1, user=user1).count() > 0:
                    allow_comment = True
            except:
                pass
            return HttpResponse(template.render({
                'com1': com1,
                'allow_edit': access_edit,
                'review': review,
                'all_trip': com_trip,
                'allow_delete_review': allow_delete_review,
                'allow_review': allow_review,
                }, request))
    except:
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

def process_edit_logo(request):
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
        company_id = request.POST.get('company_id', '')
        c1 = Company.objects.get(id=company_id)
        c1.logo.delete()
        image = request.FILES.get('image-upload', '')
        c1.logo.put(image, content_type='image/*')
        c1.save()
        return HttpResponseRedirect('/company/?company_id=' + company_id)
    return HttpResponse("Error")

def show_logo(request):
    if request.method == 'GET':
        try:
            company_id = request.GET.get('company_id', '')
            c1 = Company.objects.get(id=company_id)
            binary_img = c1.logo.read()
            if binary_img == None:
                return HttpResponseRedirect('http://placehold.it/300x300')
            return HttpResponse(binary_img, 'image/*')
        except:
            pass
    return HttpResponseRedirect('http://placehold.it/300x300')

def add_review(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    comment = request.GET.get('comment', '')
    rating = request.GET.get('rating', '')
    user = User.objects.get(id=user_id)
    company_id = request.GET.get('company_id', '')
    company = Company.objects.get(id=company_id)
    try:
        a = ReviewCompany(comment=comment, user=user, rating=rating, company=company)
        a.save()
        return HttpResponseRedirect('/company/?company_id=' + str(company.id))
    except:
        return HttpResponse('Invalid Data')
    return HttpResponse("Invalid Data")

def delete_review(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    review_id = request.GET.get('review_id','')
    review = ReviewCompany.objects.get(id=review_id)
    if str(review.user.id) == user_id:
	try:
            review.delete()
            return HttpResponseRedirect('/company/?company_id='+review.company.id)
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    elif user.is_staff:
	try:
            review.delete()
            return HttpResponseRedirect('/company/?company_id='+review.company.id)
        except DoesNotExist:
            return HttpResponse('Wrong Key')
    return HttpResponse("Invalid Data")
        

def edit_review(request):
    user_id = request.session['user_id']
    review_id = request.GET.get('review_id','')
    review = ReviewCompany.objects.get(id=review_id)
    if str(review.user.id) == user_id:
	review.comment = request.GET.get('comment', '')
        review.rating = request.GET.get('rating', '')
	review.save()
        return HttpResponseRedirect('/company/?company_id=' + str(review.company.id))
    return HttpResponse("Invalid Data")

def featured_trip(request):
    if request.method == 'GET':
        company_id = request.GET.get('company_id','')
        com1 = Company.objects.get(id=company_id)
        all_trip = Trip.objects(company=com1, active=True)
        pass_data = {
            'trip_list': all_trip,
            'the_place': com1,
            'type': 'company',
            'nav': '<a href="/company/?company_id=' + str(com1.id) + '">' + com1.name + '</a> -> Featured Trip',
        }
        template = loader.get_template('trip/featured-trip.html')
        return HttpResponse(template.render(pass_data, request))
    return HttpResponse("No Request")

def all_company(request):
    c1 = Company.objects.order_by('name')
    template = loader.get_template('company_profile/all-company.html')
    pass_data = {
            'place_list': c1,
            }
    return HttpResponse(template.render(pass_data, request))
