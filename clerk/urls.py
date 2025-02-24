from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='clerkhome'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('attendance/', views.attendance, name='attendance'),
    path('document/', views.document, name='document'),
    path('engineer/', views.engineer, name='engineer'),
    path('request/', views.request, name='request'),
    path('task/', views.task, name='task') 
    ]
