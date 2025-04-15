from django.urls import path
from .views import user_register, engineer_register, login_view,logout_view
urlpatterns = [
    path('register/user/', user_register, name='user_register'),
    path('register/engineer/', engineer_register, name='engineer_registeration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
