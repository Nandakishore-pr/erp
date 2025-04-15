from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import EngineerProfile,Profile,CustomUser,Message
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .models import UserDocument
from clerk.models import VideoCall
from django.utils.timezone import now
from django.db.models import Q


def home(request):
    return render(request, 'user/home.html')  


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
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by("timestamp")
    return render(request, 'user/document-upload.html', {"engineer_id": engineer_id,"user_id": request.user.id,"messages": messages})

def paytax(request):
    return render(request, 'user/paytax.html')

def profiledetails(request):
    video_calls = VideoCall.objects.filter(user=request.user, scheduled_time__gte=now())
    
    return render(request,'user/profiledetails.html', {"video_calls": video_calls})

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
    
