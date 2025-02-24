from django.urls import path
from . import views

urlpatterns = [
    path('engineer_home/',views.engineer_dashboard,name='engineer_home'),
    path('engineer_editprofile/', views.engineer_editprofile, name='engineer_editprofile'),
    path('document_verification/', views.document_verification, name='document_verification'),
    path('employees/', views.employees, name='employees'),
    path('doc_wrk/', views.doc_wrk, name='doc_wrk'),
    path('engineer_register/',views.engineer_register,name='engineer_register'),
]
