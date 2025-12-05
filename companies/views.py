# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required

@role_required(['company'])
def dashboard(request):
    return render(request, 'companies/supervisor-dashboard.html')

@role_required(['company'])
def supervisor_students(request):
    return render(request, "companies/supervisor-students.html")

@role_required(['company'])
def supervisor_timesheets(request):
    return render(request, "companies/supervisor-timesheets.html")

@role_required(['company'])
def supervisor_performance(request):
    return render(request, "companies/supervisor-performance.html")

@role_required(['company'])
def supervisor_ann_create(request):
    return render(request, "companies/supervisor-announcements-create.html")

@role_required(['company'])
def supervisor_ann_view(request):
    return render(request, "companies/supervisor-announcements-view.html")
