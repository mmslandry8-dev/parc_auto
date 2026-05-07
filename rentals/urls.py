from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/<int:pk>/',
        views.create_rental,
        name='create_rental'
    ),

    path(
        'my-rentals/',
        views.my_rentals,
        name='my_rentals'
    ),

    path(
        'validate/<int:pk>/',
        views.validate_rental,
        name='validate_rental'
    ),

]