from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'clerk/home.html')

def editprofile(request):
    return render(request,'clerk/editprofile.html')

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