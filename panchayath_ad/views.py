from django.shortcuts import render, get_object_or_404, redirect
from common.models import CustomUser, EngineerProfile, ClerkProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
import random
import string
import json
from clerk.models import AdminToClerkSuggestion, ClerkDocument
from engineer.models import EngineerDocument
from clerk.models import Attendance
from clerk.models import LeaveRequest  # Import LeaveRequest from the Clerk app
from django.contrib import messages
from clerk.models import Attendance
from clerk.models import LeaveRequest  # Import LeaveRequest from the Clerk app
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from user.models import TaxPayment  # Import from user app
from django.db.models import Sum
from django.utils.timezone import localdate,timedelta
from.models import AdminDocument, Notice
from user.models import Complaint 
from django.db.models import Q, Sum
from django.utils.timezone import localdate
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Message

# Create your views here.
def home(request):
    complaints = Complaint.objects.exclude(status='Resolved').order_by('-created_at')
    search_query = request.GET.get('search', '')
    ward = request.GET.get('ward')
    date = request.GET.get('date')

    if search_query:
        complaints = complaints.filter(
            Q(user__username__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(ward__icontains=search_query)
        )
    if ward:
        complaints = complaints.filter(ward=ward)
    if date:
        complaints = complaints.filter(created_at__date=date)

    paginator = Paginator(complaints, 10)
    page = request.GET.get('page')
    complaints = paginator.get_page(page)

    # Complaint dashboard stats
    resolved = Complaint.objects.filter(status="Resolved").count()
    pending = Complaint.objects.filter(status="Pending").count()
    under_review = Complaint.objects.filter(status="Under Review").count()
    wards = Complaint.objects.values_list('ward', flat=True).distinct()

    
    total_revenue = TaxPayment.objects.aggregate(total=Sum('amount'))['total'] or 0
    daily_revenue = TaxPayment.objects.filter(payment_date__date=localdate()).aggregate(total=Sum('amount'))['total'] or 0

    revenue_data = []
    labels = []
    for i in range(6, -1, -1):  # Last 7 days
        day = localdate() - timedelta(days=i)
        revenue = TaxPayment.objects.filter(payment_date__date=day).aggregate(total=Sum('amount'))['total'] or 0
        revenue_data.append(float(revenue))
        labels.append(day.strftime('%d %b'))  # Format: 14 Mar, 15 Mar, etc.
        
    return render(request,'panchayath_officer/home.html',{
        'total_revenue': total_revenue,
        'daily_revenue': daily_revenue,
        'revenue_data': revenue_data,
        'labels': labels,
        'complaints': complaints,
        'resolved': resolved,
        'pending': pending,
        'under_review': under_review,
        'wards': wards,
    })

def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        message_text = request.POST.get('message')

        if message_text:
            complaint.status = 'Resolved'
            complaint.save()

        Message.objects.create(
                sender = CustomUser.objects.get(role='admin'),
                recipient=complaint.user,
                message=message_text
            )
        messages.success(request, f"Complaint #{complaint.id} resolved successfully!")
        return redirect('admindashboard')
    else:
            messages.error(request, 'Please enter a message before submitting.')
    return render(request, 'panchayath_officer/home.html', {'complaint': complaint})

def manage(request):
    clerks = ClerkProfile.objects.select_related("user").prefetch_related("attendances").all()
    leave_requests = LeaveRequest.objects.select_related("clerk").filter(status="Pending")
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

# def revenue(request):
#     return render(request,'panchayath_officer/revenue.html')

def admin_task(request):
    return render(request, 'panchayath_officer/task.html')

def notice(request):

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        recipient = request.POST['recipient']
        date = request.POST['date']
        image = request.FILES.get('image')

        notice = Notice(
            title=title,
            description=description,
            recipient=recipient,
            date=date
        )
        
        if image:
            notice.image = image
        
        notice.save()
        messages.success(request, 'Notice Published!')
        return redirect('notice')
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

            # Send email with password
            subject = "Your Clerk Account Credentials"
            message = f"Hello {name},\n\nYour clerk account has been created successfully.\n\nLogin Details:\nEmail: {email}\nPassword: {password}\n\nPlease change your password after logging in.\n\nThank you!"
            from_email = "your_email@gmail.com"  # Replace with your Gmail ID
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

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
def leave_action(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        leave = get_object_or_404(LeaveRequest, id=leave_id)

        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        else:
            return JsonResponse({"success": False, "message": "Invalid action."})

        leave.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "message": "Invalid request."})

<<<<<<< HEAD
def tax_payments_list(request):
    today=localdate()
    daily_revenue = TaxPayment.objects.filter(payment_date__date=today).aggregate(total=Sum('amount'))['total'] or 0
    total_revenue = TaxPayment.objects.aggregate(total=Sum('amount'))['total'] or 0

    tax_payments = TaxPayment.objects.all().order_by('-payment_date')  # Fetch all tax payments
    return render(request, 'panchayath_officer/tax_payment_list.html', 
    {'tax_payments': tax_payments,
    'daily_revenue': daily_revenue,
    'total_revenue': total_revenue
    },)
=======
def send_admin_suggestion(request):
    if request.method == 'POST':
        doc_id = request.POST.get('document_id')
        text = request.POST.get('suggestion')
        doc = get_object_or_404(ClerkDocument, id=doc_id)

        AdminToClerkSuggestion.objects.create(
            document=doc,
            admin=request.user,
            clerk=doc.clerk,
            suggestion=text
        )
    return redirect('document_approval')
>>>>>>> video_and_chat
