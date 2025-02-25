from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class EngineerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'engineer'
        if commit:
            user.save()
        return user
    

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        if commit:
            user.save()
        return user
