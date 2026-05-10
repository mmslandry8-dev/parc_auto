from django.urls import path

from . import views

urlpatterns = [

    # CLIENT WEB
    path(
        'create/<int:pk>/',
        views.create_rental,
        name='create_rental'
    ),

    # HISTORIQUE
    path(
        'my-rentals/',
        views.my_rentals,
        name='my_rentals'
    ),

    # VALIDATION ADMIN
    path(
        'validate/<int:pk>/',
        views.validate_rental,
        name='validate_rental'
    ),

    # =====================================
    # LOCATION TERRAIN AGENT
    # =====================================

    path(
        'agent/create/',
        views.agent_create_rental,
        name='agent_create_rental'
    ),

    path(
        'cancel/<int:pk>/',
        views.cancel_rental,
        name='cancel_rental'
    ),

    path(
        'refuse/<int:pk>/',
        views.refuse_rental,
        name='refuse_rental'
    ),

    
]