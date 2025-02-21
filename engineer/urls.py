from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('document_verification/', views.document_verification, name='document_verification'),
    path('employees/', views.employees, name='employees'),
    path('doc_wrk/', views.doc_wrk, name='doc_wrk'),
]
