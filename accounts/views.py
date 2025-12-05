from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('/login/')

def landing_page(request):
    return render(request, "accounts/landing.html")

def register_page(request):
    return render(request, 'accounts/register.html')

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    return render(request, 'accounts/reset_password.html')

def profile_page(request):
    return render(request, 'accounts/profile_page.html')

# app/views.py
@csrf_exempt 
def login_page(request):
    error_message = None  # default, no error

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_role = request.POST.get('role')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.role != selected_role:
                error_message = "User exists but does not have the selected role."
            else:
                login(request, user)
                # Redirect based on role
                if user.role == 'student':
                    return redirect('/student/')
                elif user.role == 'instructor':
                    return redirect('/instructor/')
                elif user.role == 'company':
                    return redirect('/supervisor/')
                elif user.role == 'admin':
                    return redirect('/admin-dashboard/')
        else:
            error_message = "Invalid username or password."

    return render(request, 'accounts/login.html', {'error': error_message})
