from django.shortcuts import render, redirect, get_object_or_404
from common.models import EngineerProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash

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
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        about = request.POST.get('about')
        experience_years = request.POST.get('years_of_experience')

        # Update User model fields
        user.username = name
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

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        user = request.user  # Get the logged-in user

        # Check if the current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('engineer_editprofile')  # Redirect back to profile page

        # Validate new password and confirmation
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('engineer_editprofile')

        if current_password == new_password:
            messages.error(request, "New password cannot be the same as the current password.")
            return redirect('engineer_editprofile')

        # Update the password
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully.")
        return redirect('engineer_editprofile')  # Redirect to profile or any desired page

    return redirect('engineer_editprofile')


@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = EngineerProfile.objects.get(user=request.user)
        profile.profile_image = request.FILES['profile_image']
        profile.save()
        messages.success(request, "Profile image updated successfully.")
    else:
        messages.error(request, "Please select a valid image file.")

    return redirect('engineer_editprofile')