from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('home-gardening/', views.home_gardening, name='home_gardening'),
    path('hydroponic-gardening/', views.hydroponic_gardening, name='hydroponic_gardening'),
    path('garden-layout/',views.garden_layout, name='garden_layout'),
    path('garden-form/',views.garden_form, name='garden_form'),
    path('optimize-garden-space/',views.optimize_garden_space, name='optimize_garden_space'),
    path('optimize-garden/',views.optimize_garden,name='optimize_garden'),
    
    path('bfs-planting/',views.bfs_planting,name='bfs_planting'),
    

]
