from django.shortcuts import render, get_object_or_404, redirect
from common.models import CustomUser, EngineerProfile, ClerkProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
import random
import string
import json
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from clerk.models import ClerkDocument
from engineer.models import EngineerDocument

=======
from clerk.models import Attendance
from clerk.models import LeaveRequest  # Import LeaveRequest from the Clerk app
from django.contrib import messages
>>>>>>> Stashed changes
=======
from clerk.models import Attendance
from clerk.models import LeaveRequest  # Import LeaveRequest from the Clerk app
from django.contrib import messages
>>>>>>> Stashed changes
# Create your views here.
def home(request):
    return render(request,'panchayath_officer/home.html')

def manage(request):
    clerks = ClerkProfile.objects.select_related("user").prefetch_related("attendances").all()
    leave_requests = LeaveRequest.objects.select_related("clerk").all()
    # attendance_records = {
    #     clerk.user.id: list(clerk.attendances.all()) for clerk in clerks
    # }
    
    # for clerk in clerks:
    #      attendance_records[clerk.user.id] = list(Attendance.objects.filter(clerk=clerk))
    return render(request, 'panchayath_officer/manage.html', {
        'clerks': clerks,
        'leave_requests':leave_requests
        # 'attendance_records': attendance_records,
    })
def admin_engineer(request):
    engineers = CustomUser.objects.filter(role='engineer').select_related('engineer_profile')
    return render(request,'panchayath_officer/engineer.html',{'engineers':engineers})

@csrf_exempt
def approve_engineer(request, engineer_id):
    print(f"🔍 Received request to approve engineer {engineer_id}")

    if request.method != "POST":
        return HttpResponseNotFound("<h1>404 Not Found</h1>")

    try:
        engineer = get_object_or_404(EngineerProfile, id=engineer_id)
        engineer.is_approved = True
        engineer.save()
        return JsonResponse({'status': 'approved'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def reject_engineer(request, engineer_id):
    print(f"🔍 Received request to reject engineer {engineer_id}")

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # ✅ Use `id` instead of `user__id`
        engineer = get_object_or_404(EngineerProfile, id=engineer_id)
        user = engineer.user  

        print(f"✅ Found engineer profile: {engineer} with user ID {user.id}")

        engineer.delete()  # Delete engineer profile
        print(f"🗑 Engineer profile deleted")

        user.delete()  # Delete user
        print(f"🗑 User deleted")

        return JsonResponse({'status': 'rejected'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


    

def revenue(request):
    return render(request,'panchayath_officer/revenue.html')

def admin_task(request):
    return render(request, 'panchayath_officer/task.html')

def notice(request):
    return render(request, 'panchayath_officer/notice.html')

def admineditprofile(request):
    return render(request, 'panchayath_officer/editprofile.html')


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@csrf_exempt
def add_clerk(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            phone = data.get("phone")

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "error": "Email already exists!"})

            if CustomUser.objects.filter(phone_number=phone).exists():
                return JsonResponse({"success": False, "error": "Phone number already exists!"})

            password = generate_random_password()

            clerk = CustomUser.objects.create(
                username=name,
                email=email,
                phone_number=phone,
                role="clerk"
            )
            clerk.set_password(password)  # Hash the password
            print(password)
            clerk.save()

            return JsonResponse({"success": True, "message": "Clerk added successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})


@csrf_exempt
def delete_clerks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            clerk_ids = data.get("clerk_ids", [])

            if not clerk_ids:
                return JsonResponse({"success": False, "error": "No clerks selected."})

            # Delete selected clerks
            CustomUser.objects.filter(id__in=clerk_ids, role="clerk").delete()

            return JsonResponse({"success": True, "message": "Clerks deleted successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ClerkDocument, EngineerDocument

def document_approval(request):
    """Retrieve all clerk documents for approval"""
    clerk_documents = ClerkDocument.objects.select_related('engineer_document__user_document').all()

    context = {
        'clerk_documents': clerk_documents
    }
    return render(request, 'panchayath_officer/document_approval.html', context)

@csrf_exempt
def approve_clerk_document(request, doc_id):
    """Approve document: Change status & save to EngineerDocument"""
    if request.method == "POST":
        try:
            clerk_doc = ClerkDocument.objects.get(id=doc_id)
            # Save to EngineerDocument
            EngineerDocument.objects.create(
                engineer=clerk_doc.engineer_document.engineer,
                user_document=clerk_doc.engineer_document.user_document,
                clerk=clerk_doc.clerk,
                description=clerk_doc.description,
                additional_document=clerk_doc.additional_document,
                status=True  # Mark as verified
            )
            # Update status in ClerkDocument
            clerk_doc.status = True
            clerk_doc.save()
            return JsonResponse({"success": True})
        except ClerkDocument.DoesNotExist:
            return JsonResponse({"success": False, "error": "Document not found."})
    return JsonResponse({"success": False, "error": "Invalid request."})

@csrf_exempt
def reject_clerk_document(request, doc_id):
    """Reject document: Delete from ClerkDocument"""
    if request.method == "POST":
        try:
            document = ClerkDocument.objects.get(id=doc_id)
            document.delete()
            return JsonResponse({"success": True})
        except ClerkDocument.DoesNotExist:
            return JsonResponse({"success": False, "error": "Document not found."})
    return JsonResponse({"success": False, "error": "Invalid request."})


@csrf_exempt
def approve_leave(request, leave_id):
    if request.method=="POST":
            leave_request = get_object_or_404(LeaveRequest, id=leave_id)
            leave_request.status = "Approved"
            leave_request.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request method"})
    
# Reject Leave Request
@csrf_exempt
def reject_leave(request, leave_id):
    if request.method == "POST":
        
            leave = LeaveRequest.objects.get(id=leave_id)
            leave.status = "Rejected"
            leave.save()
            return JsonResponse({"status": "success"})
       
<<<<<<< Updated upstream
    return JsonResponse({"status": "error", "message": "Invalid request method"})
>>>>>>> Stashed changes
=======
    return JsonResponse({"status": "error", "message": "Invalid request method"})
>>>>>>> Stashed changes
