from models import *
from mongoengine import *
from mongoengine.django.auth import User as MongoUser

def add_photo():
    user1 = User.objects.get(id="581182d735f2ad11f73bfa4e")
    nutmos_photo = open('/Users/nutmos/Desktop/getavatar.php.png', 'rb')
    user1.photo.put(nutmos_photo, content_type='image/*')
    user1.save()
