from django.shortcuts import render
from common.models import CustomUser, EngineerProfile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
import random
import string
import json

# Create your views here.
def home(request):
    return render(request,'panchayath_officer/home.html')

def manage(request):
    clerks = CustomUser.objects.filter(role='clerk')
    return render(request,'panchayath_officer/manage.html',{'clerks':clerks})

def admin_engineer(request):
    engineers = CustomUser.objects.filter(role='engineer').select_related('engineer_profile')
    return render(request,'panchayath_officer/engineer.html',{'engineers':engineers})

@csrf_exempt
def approve_engineer(request, engineer_id):
    print(f"🔍 Received request to approve engineer {engineer_id}")

    if request.method != "POST":
        return HttpResponseNotFound("<h1>404 Not Found</h1>")

    try:
        engineer = get_object_or_404(EngineerProfile, id=engineer_id)
        engineer.is_approved = True
        engineer.save()
        return JsonResponse({'status': 'approved'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def reject_engineer(request, engineer_id):
    print(f"🔍 Received request to reject engineer {engineer_id}")

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        # ✅ Use `id` instead of `user__id`
        engineer = get_object_or_404(EngineerProfile, id=engineer_id)
        user = engineer.user  

        print(f"✅ Found engineer profile: {engineer} with user ID {user.id}")

        engineer.delete()  # Delete engineer profile
        print(f"🗑 Engineer profile deleted")

        user.delete()  # Delete user
        print(f"🗑 User deleted")

        return JsonResponse({'status': 'rejected'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


    

def revenue(request):
    return render(request,'panchayath_officer/revenue.html')

def admin_task(request):
    return render(request, 'panchayath_officer/task.html')

def notice(request):
    return render(request, 'panchayath_officer/notice.html')

def admineditprofile(request):
    return render(request, 'panchayath_officer/editprofile.html')


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@csrf_exempt
def add_clerk(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            phone = data.get("phone")

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"success": False, "error": "Email already exists!"})

            if CustomUser.objects.filter(phone_number=phone).exists():
                return JsonResponse({"success": False, "error": "Phone number already exists!"})

            password = generate_random_password()

            clerk = CustomUser.objects.create(
                username=name,
                email=email,
                phone_number=phone,
                role="clerk"
            )
            clerk.set_password(password)  # Hash the password
            print(password)
            clerk.save()

            return JsonResponse({"success": True, "message": "Clerk added successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})


@csrf_exempt
def delete_clerks(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            clerk_ids = data.get("clerk_ids", [])

            if not clerk_ids:
                return JsonResponse({"success": False, "error": "No clerks selected."})

            # Delete selected clerks
            CustomUser.objects.filter(id__in=clerk_ids, role="clerk").delete()

            return JsonResponse({"success": True, "message": "Clerks deleted successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})