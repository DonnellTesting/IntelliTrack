# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from .models import Class

# Dashboard
@role_required(['instructor'])
def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# Class View (ONLY ONE CLASS PER INSTRUCTOR)
@role_required(['instructor'])
def instructor_class_list(request):
    instructor = request.user

    # Get the one class assigned to the instructor
    class_obj = Class.objects.filter(instructor=instructor).first()

    # Avoid error if class doesn't exist yet
    students = class_obj.students.all() if class_obj else []

    return render(request, "teacher/teacher-class.html", {
        "class_obj": class_obj,
        "students": students,
    })

# Individual class view (OPTIONAL but still works)
@role_required(['instructor'])
def instructor_class_view(request, class_id):
    instructor = request.user

    class_obj = Class.objects.filter(id=class_id, instructor=instructor).first()
    students = class_obj.students.all() if class_obj else []

    return render(request, "teacher/teacher-class.html", {
        "class_obj": class_obj,
        "students": students,
    })

# Other Views
@role_required(['instructor'])
def instructor_timesheets(request):
    return render(request, "teacher/teacher-timesheets.html")

@role_required(['instructor'])
def instructor_performance(request):
    return render(request, "teacher/teacher-performance.html")

@role_required(['instructor'])
def instructor_placements(request):
    return render(request, "teacher/teacher-placements.html")

@role_required(['instructor'])
def instructor_announcement_create(request):
    return render(request, "teacher/teacher-announcements-create.html")

@role_required(['instructor'])
def instructor_announcement_list(request):
    return render(request, "teacher/teacher-announcements-view.html")