# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from .models import Class
from student.models import OJTPlacement
from accounts.models import Announcement
from accounts.forms import AnnouncementForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseNotAllowed

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

@role_required(['instructor'])
def instructor_timesheets(request):
    return render(request, "teacher/teacher-timesheets.html")

@role_required(['instructor'])
def instructor_performance(request):
    return render(request, "teacher/teacher-performance.html")

@role_required(['instructor'])
def instructor_announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user  # instructor becomes author
            announcement.visible_to_all = True   # instructors always visible to all
            announcement.save()
            return redirect('/instructor/announcements/view')
    else:
        form = AnnouncementForm()

    return render(request, "teacher/teacher-announcements-create.html", {
        "form": form,
    })

@role_required(['instructor'])
def instructor_announcement_list(request):
    announcements = Announcement.objects.filter(
        visible_to_all=True
    ).order_by('-created_at')

    today = timezone.localdate()

    return render(request, "teacher/teacher-announcements-view.html", {
        'announcements': announcements,
        'today': today,
    })

@role_required(['instructor'])
def instructor_announcement_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)

    # Only allow author OR admin/superuser
    if request.user != ann.author and not request.user.is_superuser:
        messages.error(request, "You cannot delete this announcement.")
        return redirect("/instructor/announcements/view")

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    ann.delete()
    messages.success(request, "Announcement deleted successfully.")
    return redirect("/instructor/announcements/view")
