# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required

@role_required(['instructor'])
def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

# Class List
def instructor_class_list(request):
    return render(request, "teacher/teacher-class.html")


# OJT
def instructor_timesheets(request):
    return render(request, "teacher/teacher-timesheets.html")

def instructor_performance(request):
    return render(request, "teacher/teacher-performance.html")

def instructor_placements(request):
    return render(request, "teacher/teacher-placements.html")


# Announcements
def instructor_announcement_create(request):
    return render(request, "teacher/teacher-announcements-create.html")

def instructor_announcement_list(request):
    return render(request, "teacher/teacher-announcements-view.html")
