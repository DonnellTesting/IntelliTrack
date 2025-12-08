# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from student.models import OJTPlacement
from student.models import OJTProgress
from accounts.models import Announcement
from accounts.forms import AnnouncementForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseForbidden

@role_required(['company'])
def dashboard(request):
    return render(request, 'companies/supervisor-dashboard.html')

@role_required(['company'])   # Only company supervisors can access
def supervisor_students(request):

    # Get all students supervised by this logged-in company supervisor
    placements = request.user.supervised_students.select_related(
        "student"
    ).order_by("student__last_name", "student__first_name")

    return render(request, "companies/supervisor-students.html", {
        "placements": placements
    })

@role_required(['company'])   # Only company supervisors can access
def supervisor_students_view(request):

    # Get all students supervised by this logged-in company supervisor
    placements = request.user.supervised_students.select_related(
        "student"
    ).order_by("student__last_name", "student__first_name")

    return render(request, "companies/supervisor-students-view.html", {
        "placements": placements
    })

@role_required(['company'])   # Only company supervisors can access
def supervisor_students_modify(request):

    # Get all students supervised by this logged-in company supervisor
    placements = request.user.supervised_students.select_related(
        "student"
    ).order_by("student__last_name", "student__first_name")

    return render(request, "companies/supervisor-students-modify.html", {
        "placements": placements
    })

@role_required(['company'])
def supervisor_timesheets_modify(request, placement_id):
    placement = get_object_or_404(
        OJTPlacement,
        id=placement_id,
        supervisor=request.user
    )

    saved = False  # flag for template

    if request.method == "POST":
        date = request.POST.get("date")
        hours = request.POST.get("hours_worked")
        rating = request.POST.get("performance_rating")
        remarks = request.POST.get("remarks")

        progress, created = OJTProgress.objects.update_or_create(
            placement=placement,
            date=date,
            defaults={
                "hours_worked": hours,
                "performance_rating": rating,
                "remarks": remarks,
                "supervisor": request.user,
            }
        )

        saved = True  # set flag

        # stay on the same page
        return render(request, "companies/supervisor-timesheets-modify.html", {
            "placement": placement,
            "saved": saved
        })

    return render(request, "companies/supervisor-timesheets-modify.html", {
        "placement": placement
    })

def supervisor_timesheets_delete(request, log_id):

    log = get_object_or_404(OJTProgress, id=log_id, supervisor=request.user)
    placement_id = log.placement.id
    log.delete()

    messages.success(request, "Timesheet entry deleted successfully.")
    return redirect('supervisor_timesheets_view', placement_id=placement_id)

@role_required(['company'])
def supervisor_timesheets_view(request, placement_id):
    placement = get_object_or_404(
        OJTPlacement,
        id=placement_id,
        supervisor=request.user  # Extra safety
    )

    logs = placement.progress_logs.all()

    return render(request, "companies/supervisor-timesheets-view.html", {
        "placement": placement,
        "logs": logs,
    })

@role_required(['company'])
def supervisor_ann_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user  # instructor becomes author
            announcement.visible_to_all = True   # instructors always visible to all
            announcement.save()
            return redirect('/supervisor/announcements/view')
    else:
        form = AnnouncementForm()

    return render(request, "companies/supervisor-announcements-create.html", {
        "form": form,
    })

@role_required(['company'])
def supervisor_ann_list(request):
    announcements = Announcement.objects.filter(
        visible_to_all=True
    ).order_by('-created_at')

    today = timezone.localdate()

    return render(request, "companies/supervisor-announcements-view.html", {
        'announcements': announcements,
        'today': today,
    })

@role_required(['company'])
def supervisor_ann_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)

    # Only allow author OR admin/superuser
    if request.user != ann.author and not request.user.is_superuser:
        messages.error(request, "You cannot delete this announcement.")
        return redirect("/supervisor/announcements/view")

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    ann.delete()
    messages.success(request, "Announcement deleted successfully.")
    return redirect("/supervisor/announcements/view")
