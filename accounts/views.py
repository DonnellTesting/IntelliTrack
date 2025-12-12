from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from student.models import OJTPlacement, OJTProgress
from datetime import date
import calendar
from django.db.models import Sum, Avg

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

    role_redirects = {
        "student": "/student/",
        "instructor": "/instructor/",
        "company": "/supervisor/",
        "admin": "/admin/",
    }

    back_url = role_redirects.get(user.role, "/") 

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
    error_message = None 

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

def timesheets_certificate(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id)

    from datetime import date
    today = date.today()

    return render(request, "accounts/timesheets-certificate.html", {
        "placement": placement,
        "today": today,
    })

def timesheets_print(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id)
    logs = placement.progress_logs.all()

    MAX_HOURS = 600

    total_hours = logs.aggregate(total=Sum('hours_worked'))['total'] or 0
    completion_pct = round(total_hours / MAX_HOURS * 100, 1)

    avg_rating = logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0
    avg_rating = round(avg_rating, 2)

    def generate_stars(rating):
        stars = ""
        for i in range(1, 6):
            stars += "★" if rating >= i else "☆"
        return stars

    star_string = generate_stars(avg_rating)

    today = date.today()

    return render(request, "accounts/timesheets-print.html", {
        "placement": placement,
        "logs": logs,
        "total_hours": total_hours,
        "completion_pct": completion_pct,
        "avg_rating": avg_rating,
        "avg_rating_stars": star_string,
        "today": today,
    })
