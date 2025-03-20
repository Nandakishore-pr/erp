from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import EngineerProfile,Profile,CustomUser
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .models import TaxPayment, UserDocument
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.timezone import localdate
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # Import for accurate month subtraction
import stripe 

from django.conf import settings
from django.shortcuts import render,redirect
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    total_revenue = TaxPayment.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0

    # Get daily revenue of the logged-in user
    daily_revenue = TaxPayment.objects.filter(user=request.user, payment_date__date=localdate()).aggregate(total=Sum('amount'))['total'] or 0

    # Get revenue data for the last 6 months
    labels = []
    revenue_data = []  # Replace with actual query data
   
    for i in range(5, -1, -1):  # Last 6 months
        month = localdate().replace(day=1) - relativedelta(months=i)  # Correct month calculation

        month_revenue = TaxPayment.objects.filter(user=request.user, payment_date__year=month.year, payment_date__month=month.month).aggregate(total=Sum('amount'))['total'] or 0
        revenue_data.append(float(month_revenue))
        labels.append(month.strftime('%b'))  # Format: Jan, Feb, etc.
        context = {
        'total_revenue': total_revenue,
        'daily_revenue': daily_revenue,
        'revenue_data': json.dumps(revenue_data),  # Ensure proper JSON format
        'labels': json.dumps(labels),  # Convert lists to JSON
    }
    return render(request, 'user/home.html',context)


def user_engineer(request):
    engineers = EngineerProfile.objects.select_related('user').all()
    return render(request, 'user/engineer.html',{'engineers':engineers })  


def report(request):
    return render(request, 'user/report.html')  


def about(request):
    return render(request, 'user/about.html') 

def employee(request):

    return render(request, 'user/employee.html') 

@login_required
def document_upload(request,engineer_id):
    return render(request, 'user/document-upload.html', {"engineer_id": engineer_id})



def profiledetails(request):
    recent_payments = TaxPayment.objects.filter(user=request.user).order_by('-payment_date')[:5]  # Last 5 payments
    return render(request,'user/profiledetails.html', {'recent_payments': recent_payments})

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
    
@login_required
def tax_payment_view(request):
    if request.method == "POST":
        tax_type = request.POST.get("tax_type")
        year = request.POST.get("year") if tax_type == "Property" else None
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")

        # Ensure required fields are present
        if not tax_type or not amount or not payment_method:
            messages.error(request, "Please fill all required fields.")
            return redirect("paytax")

        try:
            # Convert amount to cents
            stripe_amount = int(float(amount) * 100)

            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": tax_type},
                            "unit_amount": stripe_amount,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"http://127.0.0.1:8000/payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url="http://127.0.0.1:8000/payment/cancel/",
                metadata={
                    "user_id": str(request.user.id),  # Store user ID in metadata
                    "tax_type": tax_type,
                    "year": year or "",
                    "amount": amount,
                    "payment_method": payment_method,
                },
            )

            return redirect(session.url)  # Redirect user to Stripe Checkout

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment error: {str(e)}")
            return redirect("paytax")

    return render(request, "user/paytax.html")

@login_required
def success_view(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "Invalid payment session.")
        return redirect("paytax")

    try:
        # Retrieve session details from Stripe
        session = stripe.checkout.Session.retrieve(session_id)

        # Extract metadata
        user_id = session.metadata.get("user_id")
        tax_type = session.metadata.get("tax_type")
        year = session.metadata.get("year") or None
        amount = float(session.metadata.get("amount", 0))
        payment_method = session.metadata.get("payment_method")

        # Store the payment in the database after successful payment
        TaxPayment.objects.create(
            user=request.user,  # Ensure the logged-in user is assigned
            tax_type=tax_type,
            year=year,
            amount=amount,
            payment_method=payment_method,
        )

        messages.success(request, "Payment successful! Your tax details have been saved.")
        return redirect("paytax")

    except stripe.error.StripeError:
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect("paytax")

def cancel_view(request):
    messages.warning(request, "Payment was cancelled.")
    return redirect("paytax")