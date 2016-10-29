from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit/', views.edit_profile, name='edit_profile'),
    url(r'^change-password/', views.change_password, name='change_password')
]
