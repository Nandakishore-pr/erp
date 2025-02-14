from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser, Profile

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        house_number = data.get('house_number')
        ward_number = data.get('ward_number')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already taken'})
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'register.html', {'error': 'Phone number already taken'})

        user = CustomUser.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
        Profile.objects.create(user=user, house_number=house_number, ward_number=ward_number)

        return redirect('home')  # Redirect to home page after successful registration

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Logs in the user
            return redirect('home')  # Redirects to the home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})


def home(request):
    return render(request, 'base.html')  