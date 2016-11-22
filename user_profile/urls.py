from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^change-password/', views.change_password, name='change_password'),
    url(r'^image/', views.show_image, name='image'),
    url(r'^handle-change-picture/', views.handle_change_picture, name='handle-change-picture'),
    url(r'^user/(?P<user>\w+)/', views.other_user_profile, name='user'),
    #url(r'^(?P<user>\w+)', views.other_user_profile, name='user'),
]
