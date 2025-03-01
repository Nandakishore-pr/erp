from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,EngineerProfile


class EngineerRegistrationForm(UserCreationForm):
    license_number = forms.CharField(max_length=20, required=True)  # Increased max length
    license_document = forms.FileField(required=True)
    experience_years = forms.IntegerField(min_value=0, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'engineer'
        if commit:
            user.save()
            EngineerProfile.objects.create(
                user=user,
                license_number=self.cleaned_data['license_number'],
                license_document=self.cleaned_data['license_document'],
                experience_years=self.cleaned_data['experience_years'],
                is_approved=False  # Engineers must be approved before login
            )
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
