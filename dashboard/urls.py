from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # ADMIN
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    # AGENT
    path(
        'agent-dashboard/',
        views.agent_dashboard,
        name='agent_dashboard'
    ),

    # AGENT ACTIONS
    path(
        'agent/rentals/create/',
        views.agent_create_rental,
        name='agent_create_rental'
    ),

    path(
        'agent/sales/create/',
        views.agent_create_sale,
        name='agent_create_sale'    
    ),

    path(
        'operations/',
        views.operations_management,
        name='operations_management'
    ),

]