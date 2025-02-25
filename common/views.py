from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import EngineerRegistrationForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

# Role-based Registration Views
def register(request, role):
    if role == 'engineer':
        form_class = EngineerRegistrationForm
        dashboard_redirect = 'engineer_dashboard'
    # elif role == 'clerk':
    #     dashboard_redirect = 'clerk_dashboard'
    else:  # Default to user registration
        form_class = UserRegistrationForm
        dashboard_redirect = 'user_dashboard'

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role  # Assign the role before saving
            user.save()
            login(request, user)
            return redirect(dashboard_redirect)
    else:
        form = form_class()

    return render(request, 'common/register.html', {'form': form, 'role': role})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_dashboard(user)
    else:
        form = AuthenticationForm()

    return render(request, 'common/login.html', {'form': form})

# Redirect based on role
def redirect_dashboard(user):
    role_dashboard_mapping = {
        'admin': 'admin_dashboard',
        'clerk': 'clerk_dashboard',
        'engineer': 'engineer_dashboard',
        'user': 'user_dashboard',
    }
    return redirect(role_dashboard_mapping.get(user.role, 'user_dashboard'))
