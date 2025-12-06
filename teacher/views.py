# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from .models import Class
from student.models import OJTPlacement

# Dashboard
@role_required(['instructor'])
def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

#Class List
@role_required(['instructor'])
def instructor_placements(request):
    placements = OJTPlacement.objects.select_related('student', 'supervisor').all()

    return render(request, "teacher/teacher-placements.html", {
        "placements": placements
    })

# Placement View 
@role_required(['instructor'])
def instructor_class_list(request):
    placements = (
        OJTPlacement.objects
        .select_related("student")
        .order_by("company_name", "student__last_name", "student__first_name")
    )

    return render(request, "teacher/teacher-class.html", {
        "placements": placements
    })

# Other Views
@role_required(['instructor'])
def instructor_timesheets(request):
    return render(request, "teacher/teacher-timesheets.html")

@role_required(['instructor'])
def instructor_performance(request):
    return render(request, "teacher/teacher-performance.html")

@role_required(['instructor'])
def instructor_announcement_create(request):
    return render(request, "teacher/teacher-announcements-create.html")

@role_required(['instructor'])
def instructor_announcement_list(request):
    return render(request, "teacher/teacher-announcements-view.html")