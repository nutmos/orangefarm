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
    url(r'^logo/', views.show_logo, name='logo'),
    url(r'^process-edit-logo/', views.process_edit_logo, name='process-edit-logo'),
    url(r'^add-review/', views.add_review, name='add-review'),
    url(r'^featured-trip/',views.featured_trip, name='featured-trip'),
]
