from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from common.models import EngineerProfile,Profile,CustomUser
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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