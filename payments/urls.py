from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/<int:pk>/',
        views.create_payment,
        name='create_payment'
    ),

    path(
        'my-payments/',
        views.my_payments,
        name='my_payments'
    ),

    path(
        'validate/<int:pk>/',
        views.validate_payment,
        name='validate_payment'
    ),

]