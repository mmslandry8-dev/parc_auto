from django.urls import path
from . import views

urlpatterns = [

    path(
        'rental/<int:pk>/',
        views.invoice_rental,
        name='invoice_rental'
    ),

    path(
        'sale/<int:pk>/',
        views.invoice_sale,
        name='invoice_sale'
    ),

]