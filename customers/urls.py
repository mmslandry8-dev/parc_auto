from django.urls import path
from . import views

urlpatterns = [

    path(
        'list/',
        views.customer_list,
        name='customer_list'
    ),

    path(
        'detail/<int:pk>/',
        views.customer_detail,
        name='customer_detail'
    ),

]