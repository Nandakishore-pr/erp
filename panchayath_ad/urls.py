from django.urls import path
from . import views

urlpatterns = [
    
    path('admin1/', views.home, name='admindashboard'),
    path('manage/',views.manage, name='manage'),
    path('engineer/',views.engineer, name='engineer'),
    path('revenue/', views.revenue ,name='revenue'),
    path('task/',views.task ,name='task'),
    path('notice/',views.notice ,name='notice'),
    path('editprofile/',views.editprofile , name='editprofile'),
    ]

