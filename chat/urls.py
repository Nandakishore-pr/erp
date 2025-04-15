from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_message, name='send_message'),
    path('room/<str:room_name>/<str:username>/', views.chat_room, name='chat_room'),
    path('create-chat-request/<int:engineer_id>/', views.create_chat_request, name='create_chat_request'),
    path('engineer/chat-requests/', views.engineer_chat_requests, name='engineer_chat_requests'),
]
