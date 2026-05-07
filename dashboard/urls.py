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
    # path(
    #     'agent-dashboard/',
    #     views.agent_dashboard,
    #     name='agent_dashboard'
    # ),

]