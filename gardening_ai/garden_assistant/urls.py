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
    path('recommend/',views.recommend_plants_smart,name='recommend_plants_smart'), 
    path('predict/', views.predict_disease, name='predict_disease'),
    path('chatbot/',views.chatbot_page,name='chatbot_page'),
    path('chatbotmsg/',views.gardening_chatbot,name='gardening_chatbot'),
     path('garden/', views.garden_type_selection, name='garden_type_selection'),
    path('garden/dimensions/<str:garden_type>/', views.get_dimensions, name='get_dimensions'),
    path('generate-layout/', views.generate_layout, name='generate_layout'),
    
    
    path('chat-home/', views.chat_home, name='chat_home'),
    path('chat/message/', views.chat_message, name='chat_message'),

    

    

]
