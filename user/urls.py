from django.urls import path
from . import views
from .views import chatbot_response  # Import Panchayath page view

urlpatterns = [
    # path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),  # Home page route
    path('view_engineer/', views.user_engineer, name='user_engineer'),
    path('report/', views.report, name='report'),
    path('about/', views.about, name='about'),
    path('employee/', views.employee, name='employee'),
    path('document_upload/', views.document_upload, name='document_upload'),
    path('paytax/',views.paytax, name='paytax'),
    path('profiledetails',views.profiledetails ,name='profiledetails'),
    path("chatbot/", chatbot_response, name="chatbot_response"),  # Chatbot API
]
