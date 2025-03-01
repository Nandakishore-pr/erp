from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EngineerRegistrationForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import EngineerProfile
from django.core.exceptions import ValidationError


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'common/user-registration.html', {'form': form, 'role': 'user'})

# def engineer_register(request):
#     if request.method == 'POST':
#         form = EngineerRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to login after successful registration
#     else:
#         form = EngineerRegistrationForm()
#     return render(request, 'common/engineer-registraion.html', {'form': form, 'role': 'engineer'})

def engineer_register(request):
    if request.method == 'POST':
        form = EngineerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Engineer registered successfully! Please wait for admin approval.")
                return redirect('engineer_registeration')  # Redirect to avoid form resubmission on refresh
            except ValidationError as e:
                messages.error(request, e.message)  # Show the validation error message
        else:
            print("Form errors:", form.errors)  # Debugging step
            messages.error(request, "There were errors in your registration form. Please fix them below.")

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
                # 🚀 Check if the user is an engineer and requires admin approval
                if hasattr(user, 'engineer_profile') and not user.engineer_profile.is_approved:
                    messages.error(request, "Your account is not approved by the admin.")
                    return render(request, 'common/login.html', {'form': form})

                login(request, user)  # ✅ Log in the user
                return redirect_dashboard(user)  # Redirect based on role
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    return render(request, 'common/login.html', {'form': form})


def redirect_dashboard(user):
    role_dashboard_mapping = {
        'admin': 'admindashboard',
        'clerk': 'clerkhome',
        'engineer': 'engineer_home',
        'user': 'home',
    }
    return redirect(role_dashboard_mapping.get(user.role, 'user_dashboard'))
def logout_view(request):
    logout(request)
    return redirect('home')
