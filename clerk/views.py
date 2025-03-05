from django.shortcuts import render, redirect, get_object_or_404
from common.models import ClerkProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def home(request):
    return render(request,'clerk/home.html')

@login_required
def clerk_editprofile(request):
    user = request.user
    User = get_user_model()  # Get the custom user model

    # Ensure only clerks can access this page
    if user.role != 'clerk':
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')  # Redirect to home or any other page

    # Get or create the clerk profile for the logged-in user
    clerk_profile, created = ClerkProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        about = request.POST.get('about')
        position = request.POST.get('position')
        department = request.POST.get('deparment')

        # Update User model fields
        user.username = name
        user.phone_number = phone  # If phone_number exists in User model
        user.save()

        # Update ClerkProfile model fields
        clerk_profile.about = about
        clerk_profile.position = position
        clerk_profile.department = department
        clerk_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('clerk_editprofile')  # Reload the page after saving

    context = {
        'clerk_profile': clerk_profile
    }
    return render(request, 'clerk/editprofile.html', context)

@login_required
def upload_clerk_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = ClerkProfile.objects.get(user=request.user)
        profile.profile_image = request.FILES['profile_image']
        profile.save()
        messages.success(request, "Profile image updated successfully.")
    else:
        messages.error(request, "Please select a valid image file.")

    return redirect('clerk_editprofile')

def attendance(request):
    return render(request,'clerk/attendance.html')

def document(request):
    return render(request,'clerk/document.html')

def engineer(request):
    return render(request,'clerk/engineer.html')

def request(request):
    return render(request,'clerk/request.html')

def task(request):
    return render(request,'clerk/task.html')


@login_required
def clerk_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        user = request.user  # Get the logged-in user

        # Check if the current password is correct
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('clerk_editprofile')  # Redirect back to profile page

        # Validate new password and confirmation
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('clerk_editprofile')

        if current_password == new_password:
            messages.error(request, "New password cannot be the same as the current password.")
            return redirect('clerk_editprofile')

        # Update the password
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully.")
        return redirect('clerk_editprofile')  # Redirect to profile or any desired page

    return redirect('clerk_editprofile')