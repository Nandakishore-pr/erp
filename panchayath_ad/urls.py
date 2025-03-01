from django.urls import path
from . import views

urlpatterns = [
    
    path('admin1/', views.home, name='admindashboard'),
    path('manage/',views.manage, name='manage'),
    path('admin_engineer/',views.admin_engineer, name='admin_engineer'),
    path('revenue/', views.revenue ,name='revenue'),
    path('admin_task/',views.admin_task ,name='admin_task'),
    path('notice/',views.notice ,name='notice'),
    path('admineditprofile/',views.admineditprofile , name='admineditprofile'),
    path('approve_engineer/<int:engineer_id>/', views.approve_engineer, name='approve_engineer'),
    path('reject_engineer/<int:engineer_id>/', views.reject_engineer, name='reject_engineer'),
    path("add-clerk/", views.add_clerk, name="add_clerk"),
    path("delete-clerks/", views.delete_clerks, name="delete_clerks"),
]

