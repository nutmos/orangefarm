from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^process-edit/', views.process_edit, name='process-edit'),
    url(r'^process-add-photo/', views.process_add_photo, name='add-photo'),
    url(r'^add/', views.add, name='add'),
    url(r'^process-add/', views.process_add, name='process-add'),
    url(r'^picture/', views.show_image, name='picture'),
]
