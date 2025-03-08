from django.shortcuts import render, redirect, get_object_or_404
from common.models import ClerkProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance
from common.models import ClerkProfile
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from django.http import HttpResponse
import os

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

# def mark_attendance(request):
#     if request.method == "POST":
#         attendance_type = request.POST.get("attendance_type")
#         clerk_profile = ClerkProfile.objects.get(user=request.user)  # Get the ClerkProfile for the logged-in user

#         # Logic to update attendance
#         if attendance_type == "morning":
#             # Update morning attendance in the database
#             # Assuming you have a model or logic to handle this
#             attendance, created = Attendance.objects.get_or_create(clerk=clerk_profile, date=datetime.today().date(),session="Morning")
#             attendance.status = 'Present'
#             attendance.save()
#         elif attendance_type == "afternoon":
#             # Update afternoon attendance in the database
#             attendance, created = Attendance.objects.get_or_create(clerk=clerk_profile, date=datetime.today().date(),session="Afternoon")
#             attendance.afternoon_attendance = True  # Set attendance to True (or handle logic accordingly)
#             attendance.status = 'Present'
#             attendance.save()

#         # Redirect back to the attendance page
#         return redirect("attendance")

#     return render(request, "clerk/attendance.html")
def recognize_and_mark_attendance(user):
    try:
        # Fetch Clerk Profile
        print(f"Recognizing face for user: {user.username}")

        clerk_profile = ClerkProfile.objects.get(user=user)

        if not clerk_profile.profile_image:
            return "❌ No profile image found! Please upload one."

        profile_img_path = clerk_profile.profile_image.path  # Get profile image path
        print(f"Profile image path: {profile_img_path}")

        # Load Clerk's Profile Picture
        if not os.path.exists(profile_img_path):
            return "❌ Profile image file not found!"

        profile_img = face_recognition.load_image_file(profile_img_path)
        profile_encodings = face_recognition.face_encodings(profile_img)

        if len(profile_encodings) == 0:
            return "❌ No face detected in the profile image!"

        profile_encoding = profile_encodings[0]  # Extract face encoding

        # Open Webcam
        cam = cv2.VideoCapture(0)
        recognized = False

        for _ in range(30):  # Try capturing for 30 frames (about 3 seconds)
            ret, frame = cam.read()
            if not ret:
                continue

            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            live_encodings = face_recognition.face_encodings(rgb_frame)

            if len(live_encodings) > 0:
                live_encoding = live_encodings[0]
                match = face_recognition.compare_faces([profile_encoding], live_encoding, tolerance=0.5)

                if match[0]:  # Face matched
                    recognized = True
                    break  # Stop capturing

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):  # Allow user to quit
                break

        cam.release()
        cv2.destroyAllWindows()

        if recognized:
            # Get Current Date and Time
            now = datetime.now()
            today = now.date()
            current_time = now.time()

            # Determine Session
            session = "Morning" if now.hour < 12 else "Afternoon"

            # Mark Attendance
            attendance, created = Attendance.objects.get_or_create(
                clerk=clerk_profile, date=today, session=session,
                defaults={"status": "Present", "time": current_time}
            )

            if not created:
                # If attendance already exists, update the time and status
                attendance.status = "Present"
                attendance.time = current_time
                attendance.save()

            return f"✅ Attendance marked successfully for {session} at {current_time.strftime('%I:%M %p')}!"
        else:
            return "❌ Face not recognized! Try again."

    except ClerkProfile.DoesNotExist:
        return "❌ Clerk profile not found!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def mark_attendance(request):
    if request.method == "POST":
        message = recognize_and_mark_attendance(request.user)
        messages.success(request, message)  # Show message on UI
        return redirect("attendance")  # Redirect back to attendance page

    return render(request, "clerk/attendance.html")