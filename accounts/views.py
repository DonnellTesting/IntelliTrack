from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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

@login_required
def profile_page(request):
    user = request.user

    # Map roles to their dashboards
    role_redirects = {
        "student": "/student/",
        "instructor": "/instructor/",
        "company": "/company/",
        "admin": "/admin/",
    }

    back_url = role_redirects.get(user.role, "/")  # fallback = home

    return render(request, "accounts/profile_page.html", {
        "back_url": back_url
    })

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            messages.success(request, "Your password was updated successfully!")
            return redirect("profile")  # back to profile page
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/change_password.html", {
        "form": form
    })

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
