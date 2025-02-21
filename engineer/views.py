from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'engineer/home.html')

def editprofile(request):
    return render(request, 'engineer/editprofile.html')

def employees(request):
    return render(request, 'engineer/employees.html')

def doc_wrk(request):
    return render(request,'engineer/doc_wrk.html')

def document_verification(request):
    return render(request,'engineer/document_verification.html')

def editprofile(request):
    return render(request,'engineer/editprofile.html')

def register(request):
    return render(request, 'engineer/registration.html')