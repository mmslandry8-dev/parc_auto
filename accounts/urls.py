from django.urls import path
from . import views

urlpatterns = [

    # REGISTER
    path('register/', views.register, name='register'),

    # LOGIN
    path('login/', views.login_view, name='login'),

    # LOGOUT
    path('logout/', views.logout_view, name='logout'),


]