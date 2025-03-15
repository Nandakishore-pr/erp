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

from engineer.models import EngineerDocument
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ClerkDocument
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from django.http import HttpResponse
import os
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from django.http import HttpResponse
import os
from .models import LeaveRequest
from django.utils.dateparse import parse_date

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

def document(request):
    clerk_id = request.user.id  # Get the logged-in clerk's ID
    
    # Fetch documents assigned to this clerk
    documents = EngineerDocument.objects.filter(clerk_id=clerk_id).select_related("engineer", "user_document")

    return render(request,'clerk/document.html',{"documents": documents})


@csrf_exempt
def verify_document(request, document_id):
    if request.method == "POST":
        document = get_object_or_404(EngineerDocument, id=document_id)
        document.status = True
        document.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def reject_document(request, document_id):
    if request.method == "DELETE":
        document = get_object_or_404(EngineerDocument, id=document_id)
        document.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
def submit_clerk_document(request):
    print('inside function')
    if request.method == "POST":
        document_id = request.POST.get("documentSelect")
        final_remarks = request.POST.get("finalRemarks")
        additional_document = request.FILES.get("additional_document")

        # Ensure a document is selected
        if not document_id:
            messages.error(request, "Please select a document.")
            return redirect("document")  # Update with your actual template name

        engineer_document = get_object_or_404(EngineerDocument, id=document_id)

        # Save the ClerkDocument entry
        ClerkDocument.objects.create(
            clerk=request.user,
            engineer_document=engineer_document,
            additional_document=additional_document,
            description=final_remarks,
            status=False  # Default status
        )

        messages.success(request, "Document submitted successfully!")
        return redirect("document")  # Update with your actual template name

    # Fetch documents for display
    documents = EngineerDocument.objects.filter(clerk=request.user)
    return render(request, "clerk/document.html", {"documents": documents})

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

def attendance(request):
    clerk_profile = ClerkProfile.objects.get(user=request.user)
    today = timezone.now().date()

    # Fetch morning and afternoon attendance records
    morning_attendance = Attendance.objects.filter(clerk=clerk_profile, date=today, session="Morning").first()
    afternoon_attendance = Attendance.objects.filter(clerk=clerk_profile, date=today, session="Afternoon").first()
    leave_requests = LeaveRequest.objects.filter(clerk=clerk_profile) # Fetch all leave requests

    context = {
        "morning_attendance": morning_attendance.status if morning_attendance else None,
        "morning_time": morning_attendance.time.strftime("%I:%M %p") if morning_attendance else None,
        "afternoon_attendance": afternoon_attendance.status if afternoon_attendance else None,
        "afternoon_time": afternoon_attendance.time.strftime("%I:%M %p") if afternoon_attendance else None,
        "leave_requests":leave_requests
    }
    
    return render(request, "clerk/attendance.html", context)

def request_leave(request):
    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        reason = request.POST.get("reason")

        if leave_date and reason:
            try:
                # Get the ClerkProfile associated with the logged-in user
                clerk_profile = ClerkProfile.objects.get(user=request.user)

                LeaveRequest.objects.create(
                    clerk=clerk_profile,  # Assign ClerkProfile instance
                    date=parse_date(leave_date),
                    reason=reason,
                    status="Pending"
                )
                messages.success(request, "Your leave request has been submitted successfully.")
            except ClerkProfile.DoesNotExist:
                messages.error(request, "Clerk profile not found. Please contact the admin.")
        else:
            messages.error(request, "Please fill out all fields.")

        return redirect("attendance")  # Redirect back to attendance page

    return render(request, "attendance.html")

# def leave_status(request):
    
#     leave_requests = LeaveRequest.objects.filter(user=request.user) # Fetch all leave requests
#     print(leave_requests)
#     return render(request, 'clerk/attendance.html', {'leave_requests': leave_requests})

