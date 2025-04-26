from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('harvesthub/', views.harvesthub, name='harvesthub'),
     path('sell/', views.sell_item, name='sell_item'),
    path('buy/', views.buy_items, name='buy_items'),



    path('home-gardening/', views.home_gardening, name='home_gardening'),




    path('hydroponic-gardening/', views.hydroponic_gardening, name='hydroponic_gardening'),
    path('hydroponic-methods/', views.hydroponic_methods, name='hydroponic_methods'),
    path('hydroponic-layout/', views.hydroponic_layout, name='hydroponic_layout'),
    path('select-type-hydroponic/', views.select_type_hydroponic, name='select_type_hydroponic'),
    path('select-details-hydroponic/', views.select_details_hydroponic, name='select_details_hydroponic'),
    path('hydroponic-layout-result/', views.hydroponic_layout_result, name='hydroponic_layout_result'),
    
    path('plant_recommendation/', views.plant_recommendation, name='plant_recommendation'),
    path('plant-info/', views.plant_info, name='plant_info'),



















    path('bfs-planting/',views.bfs_planting,name='bfs_planting'),
    path('recommend/',views.recommend_plants_smart,name='recommend_plants_smart'), 
    path('predict/', views.predict_disease, name='predict_disease'),
    path('chatbot/',views.chatbot_page,name='chatbot_page'),
    path('chatbotmsg/',views.gardening_chatbot,name='gardening_chatbot'),
     path('garden/', views.garden_type_selection, name='garden_type_selection'),
    path('garden/dimensions/<str:garden_type>/', views.get_dimensions, name='get_dimensions'),
    path('generate-layout/', views.generate_layout, name='generate_layout'),
    
    
    path('chat-home/', views.chat_home, name='chat_home'),
    path('chat-message/', views.chat_message, name='chat_message'),

    

    

]
