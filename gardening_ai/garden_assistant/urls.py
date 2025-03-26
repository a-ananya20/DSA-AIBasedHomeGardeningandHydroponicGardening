from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('home-gardening/', views.home_gardening, name='home_gardening'),
    path('hydroponic-gardening/', views.hydroponic_gardening, name='hydroponic_gardening'),
]
