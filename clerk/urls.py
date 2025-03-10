from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='clerkhome'),
    path('editprofile/', views.clerk_editprofile, name='clerk_editprofile'),
    path('attendance/', views.attendance, name='attendance'),
    path('mark_attendance/',views.mark_attendance,name = 'mark_attendance'),
    path('document/', views.document, name='document'),
    path('engineer/', views.engineer, name='engineer'),
    path('request/', views.request, name='request'),
    path('task/', views.task, name='task'),
    path('clerk-change-password/', views.clerk_change_password, name='clerk_change_password'),
    path('upload-profile-image/', views.upload_clerk_profile_image, name='upload_clerk_profile_image'),

    ]
