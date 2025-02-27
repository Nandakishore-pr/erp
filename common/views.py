from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EngineerRegistrationForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'common/user-registration.html', {'form': form, 'role': 'user'})

def engineer_register(request):
    if request.method == 'POST':
        form = EngineerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = EngineerRegistrationForm()
    return render(request, 'common/engineer-registraion.html', {'form': form, 'role': 'engineer'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_dashboard(user)  # Redirect based on role
    else:
        form = AuthenticationForm()
    return render(request, 'common/login.html', {'form': form})

def redirect_dashboard(user):
    role_dashboard_mapping = {
        'admin': 'admindashboard',
        'clerk': 'clerk_dashboard',
        'engineer': 'engineer_home',
        'user': 'home',
    }
    return redirect(role_dashboard_mapping.get(user.role, 'user_dashboard'))

def logout_view(request):
    logout(request)
    return redirect('home')