from django.urls import path
from . import views

urlpatterns = [

    path(
        'add/<int:pk>/',
        views.add_maintenance,
        name='add_maintenance'
    ),

    path(
        'list/',
        views.maintenance_list,
        name='maintenance_list'
    ),

    path(
        'close/<int:pk>/',
        views.close_maintenance,
        name='close_maintenance'
    ),

]