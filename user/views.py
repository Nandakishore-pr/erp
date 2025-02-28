from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import EngineerProfile,Profile,CustomUser
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from .models import CustomUser, Profile

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         password = request.POST.get('password')
#         house_number = request.POST.get('house_number')
#         ward_number = request.POST.get('ward_number')

#         # Ensure email is provided
#         if not email:
#             messages.error(request, 'Email is required.')
#             return redirect('register')

#         # Check if user exists
#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, 'Username already taken')
#             return redirect('register')

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, 'Email already taken')
#             return redirect('register')

#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, 'Phone number already taken')
#             return redirect('register')

#         # Create the user
#         user = CustomUser.objects.create_user(
#             username=username, 
#             email=email, 
#             phone_number=phone_number, 
#             password=password
#         )
#         Profile.objects.create(user=user, house_number=house_number, ward_number=ward_number)

#         messages.success(request, 'Registration successful. Please log in.')
#         return redirect('login')

#     return render(request, 'user/register.html')


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')  
#         else:
#             messages.error(request, 'Invalid credentials')
#             return redirect('login')

#     return render(request, 'user/login.html')


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


def document_upload(request) :
    return render(request, 'user/document-upload.html')

def paytax(request):
    return render(request, 'user/paytax.html')

def profiledetails(request):
    return render(request,'user/profiledetails.html')
    
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