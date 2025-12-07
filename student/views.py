# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from student.models import OJTPlacement
from accounts.models import Announcement
from django.utils import timezone

@role_required(['student'])
def dashboard(request):
    return render(request, 'student/student-dashboard.html')

@role_required(['student'])
def student_timesheet(request):
    return render(request, "student/student-timesheet.html")

@role_required(['student'])
def student_performance(request):
    return render(request, "student/student-performance.html")

@role_required(['student'])
def student_placement(request):
    return render(request, "student/student-placement.html")

@role_required(['student'])
def student_announcements(request):
    announcements = Announcement.objects.filter(
        visible_to_all=True
    ).order_by('-created_at')

    today = timezone.localdate()

    return render(request, "student/student-announcements.html", {
        'announcements': announcements,
        'today': today,
    })