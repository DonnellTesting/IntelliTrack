# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required

@role_required(['instructor'])
def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# Class List
@role_required(['instructor'])
def instructor_class_list(request):
    return render(request, "teacher/teacher-class.html")


# OJT
@role_required(['instructor'])
def instructor_timesheets(request):
    return render(request, "teacher/teacher-timesheets.html")

@role_required(['instructor'])
def instructor_performance(request):
    return render(request, "teacher/teacher-performance.html")

@role_required(['instructor'])
def instructor_placements(request):
    return render(request, "teacher/teacher-placements.html")


# Announcements
@role_required(['instructor'])
def instructor_announcement_create(request):
    return render(request, "teacher/teacher-announcements-create.html")

@role_required(['instructor'])
def instructor_announcement_list(request):
    return render(request, "teacher/teacher-announcements-view.html")
