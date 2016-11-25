from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add_trip, name='add-trip'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^process-add/', views.process_add, name='process-add'),
    url(r'^process-edit/', views.process_edit, name='process-edit'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^show-place/', views.show_place, name='edit-place'),
    url(r'^add-place/', views.add_place, name='add-place'),
    url(r'^process-add-place/', views.process_add_place, name='process-add-place'),
    url(r'^delete-place/', views.delete_place, name='delete-place'),
    url(r'^process-delete-place/', views.process_delete_place, name='process-delete-place'),
    url(r'^featured/', views.featured_trip, name='featured'),
    url(r'^process-booking/', views.process_booking, name='process-booking'),
    url(r'^picture/',views.show_image, name='picture'),
    url(r'^handle-change-picture/', views.handle_change_picture, name='handle-change-picture'),
]
