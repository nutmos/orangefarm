from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/',views.add_place, name='add-place'),
    url(r'^edit/', views.edit, name='edit'),
    url(r'^process-add/', views.process_add, name='process-add'),
    url(r'^process-edit/', views.process_edit, name='process-edit'),
    url(r'^delete/', views.delete, name='delete'),
    url(r'^add-picture/', views.add_picture, name='add-picture'),
    url(r'^handle-add-picture/', views.handle_add_picture, name='handle-add-picture'),
    url(r'^delete-picture/', views.delete_picture, name='delete-picture'),
    url(r'^handle-delete-picture/', views.handle_delete_picture, name='handle-delete-picture'),
    url(r'^picture/', views.show_image, name='picture'),
]

