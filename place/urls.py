from django.conf.urls import url, include

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
    url(r'^edit-picture/', views.edit_picture, name='edit-picture'),
    url(r'^handle-delete-picture/', views.handle_delete_picture, name='handle-delete-picture'),
    url(r'^picture/', views.show_image, name='picture'),
    url(r'^get-place-by-city/', views.get_place_by_city, name='get-place-by-city'),
    url(r'^all/', views.all_place, name='all-place'),
    url(r'^add-review/', views.add_review, name='add-review'),
    url(r'^delete-review', views.delete_review, name='delete-review'),
    url(r'^c/(?P<place_name>\w+)/', include([
        url(r'^featured-trip/', views.featured_trip, name="featured-trip"),
        url(r'^related/', include([
            url(r'^delete/', views.delete_related, name="delete-related"),
            url(r'^process-delete/', views.process_delete_related, name="process-delete-related"),
            url(r'^add/', views.add_related, name="add-related"),
            url(r'^process-add-related/', views.process_add_related, name="process-add-related"),
            url(r'^$', views.show_related, name="related"),
        ])),
        url(r'^$', views.place_name, name='place_name'),
    ])),
]

