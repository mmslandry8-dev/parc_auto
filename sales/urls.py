from django.urls import path
from . import views

urlpatterns = [

    path(
        'request/<int:pk>/',
        views.request_sale,
        name='request_sale'
    ),

    path(
        'my/',
        views.my_sales,
        name='my_sales'
    ),

    path(
        'list/',
        views.sales_list,
        name='sales_list'
    ),

    path(
        'validate/<int:pk>/',
        views.validate_sale,
        name='validate_sale'
    ),

    path(
        'pay/<int:pk>/',
        views.pay_sale,
        name='pay_sale'
    ),

]