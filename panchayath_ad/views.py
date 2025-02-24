from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'panchayath_officer/home.html')

def manage(request):
    return render(request,'panchayath_officer/manage.html')

def engineer(request):
    return render(request,'panchayath_officer/engineer.html')

def revenue(request):
    return render(request,'panchayath_officer/revenue.html')

def task(request):
    return render(request, 'panchayath_officer/task.html')

def notice(request):
    return render(request, 'panchayath_officer/notice.html')

def editprofile(request):
    return render(request, 'panchayath_officer/editprofile.html')