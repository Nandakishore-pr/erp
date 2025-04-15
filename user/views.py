from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import EngineerProfile,Profile,CustomUser,Message
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.utils.timezone import now
from clerk.models import VideoCall,ClerkDocument
from .models import Complaint, TaxPayment, UserDocument
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.timezone import localdate
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # Import for accurate month subtraction
import stripe 
from decimal import Decimal
from panchayath_ad.models import AdminDocument, Message, Notice  # Import the model
from common.models import CustomUser  # or your actual app name
=======
from .models import UserDocument
from clerk.models import VideoCall
from django.utils.timezone import now
from django.db.models import Q
>>>>>>> video_and_chat

from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

# def home(request):
#     total_revenue = TaxPayment.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0

#     # Get daily revenue of the logged-in user
#     daily_revenue = TaxPayment.objects.filter(user=request.user, payment_date__date=localdate()).aggregate(total=Sum('amount'))['total'] or 0

#     # Get revenue data for the last 6 months
#     labels = []
#     revenue_data = []  # Replace with actual query data
   
#     for i in range(5, -1, -1):  # Last 6 months
#         month = localdate().replace(day=1) - relativedelta(months=i)  # Correct month calculation

#         month_revenue = TaxPayment.objects.filter(user=request.user, payment_date__year=month.year, payment_date__month=month.month).aggregate(total=Sum('amount'))['total'] or 0
#         revenue_data.append(float(month_revenue))
#         labels.append(month.strftime('%b'))  # Format: Jan, Feb, etc.
#         context = {
#         'total_revenue': total_revenue,
#         'daily_revenue': daily_revenue,
#         'revenue_data': json.dumps(revenue_data),  # Ensure proper JSON format
#         'labels': json.dumps(labels),  # Convert lists to JSON
#     }
#     return render(request, 'user/home.html',context)
def home(request):
    notices = Notice.objects.filter(
        recipient__in=['public', 'everyone'],
        date__lte=date.today()
    ).order_by('-date')[:5]  
    return render(request, 'user/home.html',{'notices': notices})

def user_engineer(request):
    engineers = EngineerProfile.objects.select_related('user').all()
    return render(request, 'user/engineer.html',{'engineers':engineers })  


# def report(request):
#     return render(request, 'user/report.html')  


def about(request):
    return render(request, 'user/about.html') 

def employee(request):
    employees = CustomUser.objects.exclude(role='user').select_related('engineer_profile', 'clerk_profile')

    return render(request, 'user/employee.html', {'employees': employees}) 

@login_required
def document_upload(request,engineer_id):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by("timestamp")
    return render(request, 'user/document-upload.html', {"engineer_id": engineer_id,"user_id": request.user.id,"messages": messages})



def profiledetails(request):
<<<<<<< HEAD
    user = request.user
    messages = Message.objects.filter(recipient=user).order_by('-sent_at')
    documents = ClerkDocument.objects.all()  # Fetch all records
    recent_payments = TaxPayment.objects.filter(user=request.user).order_by('-payment_date')[:5]  # Last 5 payments
    video_calls = VideoCall.objects.filter(user=request.user, scheduled_time__gte=now())
    return render(request,'user/profiledetails.html', {'recent_payments': recent_payments,'video_calls':video_calls,"documents": documents,'messages': messages})
=======
    video_calls = VideoCall.objects.filter(user=request.user, scheduled_time__gte=now())
    
    return render(request,'user/profiledetails.html', {"video_calls": video_calls})
>>>>>>> video_and_chat

@login_required
def upload_document(request):
    if request.method == "POST":
        document = request.FILES.get("document")
        description = request.POST.get("description")
        engineer_id = request.POST.get("engineer_id")  # Get engineer ID from form

        if document and engineer_id:
            engineer = CustomUser.objects.get(id=engineer_id)  # Fetch engineer
            UserDocument.objects.create(user=request.user, engineer=engineer, document=document, description=description)
            messages.success(request, "Document uploaded successfully! Wait for engineer's approval.")
            return redirect("document_upload", engineer_id=engineer.id)

        messages.error(request, "Failed to upload document. Please try again.")

    return redirect("document_upload")

@login_required
def edit_profile(request):

    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")

        profile, created = Profile.objects.get_or_create(user=user)
        profile.address = request.POST.get("address")
        profile.house_number = request.POST.get("house_number")
        profile.ward_number = request.POST.get("ward_number")
        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profiledetails")  # Change 'profile' to your profile view name

    return redirect("profiledetails")  # Redirect if not POST
    
responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm just a bot, but I'm good!", "I'm here to assist you."],
    "bye": ["Goodbye!", "See you later!", "Take care!"]
}
@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()
        
        bot_reply = responses.get(user_message, ["I'm not sure, but I'm learning!"])
        return JsonResponse({"response": random.choice(bot_reply)})
    
<<<<<<< HEAD

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import TaxPayment

# Set your Stripe secret key

@login_required
def tax_payment_view(request):
    tax_payment = TaxPayment.objects.filter(user=request.user).last()  # Get latest tax payment (if exists)
    if request.method == "POST":
        tax_type = request.POST.get("tax_type")
        year = request.POST.get("year") if tax_type == "Property" else None
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")

        if not tax_type or not amount or not payment_method:
            messages.error(request, "Please fill all required fields.")
            return redirect("paytax")

        try:
            amount_decimal = Decimal(amount)  # Ensure it’s in Decimal format

            # Create a tax payment entry with "Pending" status
            tax_payment = TaxPayment.objects.create(
                user=request.user,
                tax_type=tax_type,
                year=year if year else None,
                amount=amount,
                payment_method="Stripe",
                status="Pending"  # New field to track payment status
            )

            tax_payment.save()
            # Redirect user to Stripe checkout with tax payment ID
            return redirect("paytax")

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("paytax")

    return render(request, "user/paytax.html", {"tax_payment": tax_payment})

@csrf_exempt
def create_checkout_session(request, tax_payment_id):

    try:
        print("Fetching tax payment details...")

        tax_payment = TaxPayment.objects.get(id=tax_payment_id)
        amount_in_cents = int(float(tax_payment.amount) * 100)  # Convert to cents
        print("Creating Stripe session...")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Tax Payment - {tax_payment.tax_type}"},
                        "unit_amount": amount_in_cents,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://127.0.0.1:8000/payment/success/{tax_payment.id}/",
            cancel_url=f"http://127.0.0.1:8000/payment/cancel/{tax_payment.id}/",
        )
        print("Stripe session created successfully.")

        return JsonResponse({"id": session.id})

    except TaxPayment.DoesNotExist:
        return JsonResponse({"error": "Invalid payment ID"}, status=404)

    except Exception as e:
        print(f"Stripe error: {e}")

        return JsonResponse({"error": str(e)}, status=500)

@login_required
def success_view(request, tax_payment_id):
    try:
        tax_payment = TaxPayment.objects.get(id=tax_payment_id, user=request.user)
        tax_payment.status = "Success"  # Mark payment as completed
        tax_payment.save()

        messages.success(request, "Payment successful!")
        return redirect("paytax")

    except TaxPayment.DoesNotExist:
        messages.error(request, "Invalid transaction.")
        return redirect("paytax")

@login_required
def cancel_view(request, tax_payment_id):
    try:
        tax_payment = TaxPayment.objects.get(id=tax_payment_id, user=request.user)
        tax_payment.status = "Cancelled"  # Mark payment as cancelled
        tax_payment.save()

        messages.error(request, "Payment was cancelled.")
        return redirect("paytax")

    except TaxPayment.DoesNotExist:
        messages.error(request, "Invalid transaction.")
        return redirect("paytax")

@login_required
def register_complaint(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        ward = request.POST.get('ward')
        # name = request.POST.get('name')
        # phone = request.POST.get('phone')
        image = request.FILES.get('image')  # Optional
        description = request.POST.get('description')

        Complaint.objects.create(
            user=request.user,
            category=category,
            ward=ward,
            # name=name,
            # phone=phone,
            image=image,
            description=description
        )

        messages.success(request, "Complaint submitted successfully!")
        return redirect('report')  # Change to your user home URL name

    return render(request, 'user/report.html')
=======
>>>>>>> video_and_chat
