from django.urls import path
from . import views

urlpatterns = [
    path('engineer_home/',views.engineer_dashboard,name='engineer_home'),
    path('engineer_editprofile/', views.engineer_editprofile, name='engineer_editprofile'),
    path('document_verification/', views.document_verification, name='document_verification'),
    path("update-document-status/<int:document_id>/<str:status>/", views.update_document_status, name="update-document-status"), 
    path('employees/', views.employees, name='employees'),
    path('doc_wrk/', views.doc_wrk, name='doc_wrk'),
    path('change-password/', views.change_password, name='change_password'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('message/',views.message,name='message'),
    path("engineer-chat/", views.engineer_chat_view, name="engineer-chat"),
    path("doc-approved/", views.doc_approved, name="doc-approved"),

 ]
