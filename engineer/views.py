from django.shortcuts import render, redirect, get_object_or_404
from common.models import EngineerProfile,CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from user.models import UserDocument
from django.http import JsonResponse
from .models import EngineerDocument
# Create your views here.
def message(request):
    return render(request,'engineer/message.html')

def engineer_dashboard(request):
    return render(request,'engineer/home.html')

def editprofile(request):
    return render(request, 'engineer/editprofile.html')

def employees(request):
    clerks = CustomUser.objects.filter(role='clerk')
    return render(request, 'engineer/employees.html',{"clerks":clerks})
from django.contrib import messages

@login_required
def doc_wrk(request):
    engineer_id = request.user.id

    # Fetch documents assigned to the engineer by the user
    documents = UserDocument.objects.filter(engineer_id=engineer_id, status=True).select_related("user")
    clerks = CustomUser.objects.filter(role='clerk')

    if request.method == "POST":
        document_id = request.POST.get("document_id")
        clerk_id = request.POST.get("clerk_id")
        additional_document = request.FILES.get("additional_document")
        description = request.POST.get("description")

        if document_id and clerk_id and additional_document:
            user_document = UserDocument.objects.get(id=document_id)
            clerk = CustomUser.objects.get(id=clerk_id)

            # Save to EngineerDocument model
            EngineerDocument.objects.create(
                engineer=request.user,
                user_document=user_document,
                clerk=clerk,
                additional_document=additional_document,
                description=description
            )

            messages.success(request, "Document successfully assigned to the clerk.")
            return redirect("doc_wrk")

        messages.error(request, "Please fill in all required fields.")

    return render(request, 'engineer/doc_wrk.html', {"documents": documents, "clerks": clerks})

@login_required
def document_verification(request):
    engineer_id = request.user.id  # Assuming the logged-in engineer is a CustomUser instance
    documents = UserDocument.objects.filter(engineer_id=engineer_id).select_related("user")
    return render(request,'engineer/document_verification.html',{"documents": documents})


@login_required
def update_document_status(request, document_id, status):
    document = get_object_or_404(UserDocument, id=document_id, engineer=request.user)

    if status == "approve":
        document.status = True
        document.save()
        return JsonResponse({"success": True, "status": True})
    
    elif status == "reject":
        document.delete()
        return JsonResponse({"success": True, "status": False})

    return JsonResponse({"success": False})


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