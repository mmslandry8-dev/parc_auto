from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.vehicle_list,
        name='vehicle_list'
    ),

    path(
        'add/',
        views.add_vehicle,
        name='add_vehicle'
    ),

    path(
        '<int:pk>/',
        views.vehicle_detail,
        name='vehicle_detail'
    ),

    path(
        '<int:pk>/delete/',
        views.delete_vehicle,
        name='delete_vehicle'
    ),

    path(
        '<int:pk>/update/',
        views.update_vehicle,
        name='update_vehicle'
    ),

]