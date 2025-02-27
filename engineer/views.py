from django.shortcuts import render, redirect, get_object_or_404
from common.models import EngineerProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Create your views here.

def engineer_dashboard(request):
    return render(request,'engineer/home.html')

def editprofile(request):
    return render(request, 'engineer/editprofile.html')

def employees(request):
    return render(request, 'engineer/employees.html')

def doc_wrk(request):
    return render(request,'engineer/doc_wrk.html')

def document_verification(request):
    return render(request,'engineer/document_verification.html')

@login_required
def engineer_editprofile(request):
    user = request.user
    User = get_user_model()  # Get the custom user model

    # Ensure only engineers can access this page
    if user.role != 'engineer':
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')  # Redirect to home or any other page

    # Get or create the engineer profile for the logged-in user
    engineer_profile, created = EngineerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        about = request.POST.get('about')
        experience_years = request.POST.get('years_of_experience')

        # Update User model fields
        user.username = name
        user.email = email
        user.phone_number = phone  # If phone_number exists in User model
        user.save()

        # Update EngineerProfile model fields
        engineer_profile.address = address
        engineer_profile.about = about
        if experience_years:
            engineer_profile.experience_years = int(experience_years)
        engineer_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('engineer_editprofile')  # Reload the page after saving

    context = {
        'engineer_profile': engineer_profile
    }
    return render(request, 'engineer/editprofile.html', context)

def engineer_register(request):
    return render(request, 'engineer/regist.html')