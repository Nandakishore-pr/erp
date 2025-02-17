from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),  # Home page route
    path('engieer/', views.engineer, name='engineer'),
    path('report/', views.report, name='report'),
    path('about/', views.about, name='about'),
    path('employee/', views.employee, name='employee'),
]
