from django.urls import path
from . import views
from .views import chatbot_response, create_checkout_session, tax_payment_view  # Import Panchayath page view
from .views import success_view
urlpatterns = [
    # path('register/', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),  # Home page route
    path('view_engineer/', views.user_engineer, name='user_engineer'),
    path('report/', views.register_complaint, name='report'),
    path('about/', views.about, name='about'),
    path('employee/', views.employee, name='employee'),
    path('document_upload/<int:engineer_id>/', views.document_upload, name='document_upload'),
<<<<<<< HEAD
    path('paytax/',views.tax_payment_view, name='paytax'),
=======
    path('paytax/',views.paytax, name='paytax'),
>>>>>>> video_and_chat
    path('profiledetails/', views.profiledetails, name='profiledetails'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("upload/", views.upload_document, name="upload_document"),
    path("chatbot/", chatbot_response, name="chatbot_response"),  # Chatbot API
    path("create-checkout-session/<int:tax_payment_id>/", create_checkout_session, name="create_checkout_session"),

    path("payment/success/<int:tax_payment_id>/", success_view, name="payment_success"),
    path("payment/cancel/", views.cancel_view, name="payment_cancel"),
    path("paytax/", tax_payment_view, name="paytax"),
    # path("payment/cancel/", cancel_view, name="payment_cancel"),
]
