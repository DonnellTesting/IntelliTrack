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
from datetime import date
import calendar
from django.db.models import Sum, Avg

@role_required(['company'])
def dashboard(request):
    # Get all students under this supervisor's company
    students = OJTPlacement.objects.all()  # Adjust if filtering by company

    total_students = students.count()

    # Class total hours / max hours per student
    MAX_HOURS = 600
    total_hours = OJTProgress.objects.aggregate(total=Sum('hours_worked'))['total'] or 0
    class_completion_pct = round(total_hours / (total_students * MAX_HOURS) * 100, 1) if total_students else 0

    # Average rating for entire class
    avg_rating = OJTProgress.objects.aggregate(avg=Avg('performance_rating'))['avg'] or 0
    avg_rating_pct = round(avg_rating / 5 * 100, 1)

    # Star generator
    def generate_stars(rating):
        stars = ""
        for i in range(1, 6):
            if rating >= i:
                stars += "★"
            elif rating >= i - 0.5:
                stars += "☆"
            else:
                stars += "☆"
        return stars

    avg_rating_stars = generate_stars(avg_rating)

    # Helper: generate initials from name
    def get_initials(fullname: str):
        parts = fullname.split()
        if len(parts) == 0:
            return ""
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    # Individual student data
    student_data = []
    for student in students:
        full_name = student.student.get_full_name()
        initials = get_initials(full_name)

        progress_logs = student.progress_logs.all()
        student_hours = progress_logs.aggregate(total=Sum('hours_worked'))['total'] or 0
        student_avg_rating = progress_logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0

        student_data.append({
            'name': full_name,
            'initials': initials,
            'hours': student_hours,
            'completion_pct': round(student_hours / MAX_HOURS * 100, 1),
            'completion_remaining': round(100 - (student_hours / MAX_HOURS * 100), 1),
            'avg_rating': round(student_avg_rating, 2),
            'avg_rating_stars': generate_stars(student_avg_rating),
        })

    context = {
        'total_students': total_students,
        'class_completion_pct': class_completion_pct,
        'class_completion_remaining': 100 - class_completion_pct,
        'avg_rating': round(avg_rating, 2),
        'avg_rating_stars': avg_rating_stars,
        'student_data': student_data,
    }

    return render(request, 'companies/supervisor-dashboard.html', context)

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
        supervisor=request.user
    )

    logs = placement.progress_logs.all()

    MAX_HOURS = 600

    total_hours = logs.aggregate(total=Sum('hours_worked'))['total'] or 0
    completion_pct = round(total_hours / MAX_HOURS * 100, 1)

    avg_rating = logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0
    avg_rating = round(avg_rating, 2)

    def generate_stars(rating):
        stars = ""
        for i in range(1, 5 + 1):
            if rating >= i:
                stars += "★"
            else:
                stars += "☆"
        return stars

    star_string = generate_stars(avg_rating)

    return render(request, "companies/supervisor-timesheets-view.html", {
        "placement": placement,
        "logs": logs,
        "total_hours": total_hours,
        "completion_pct": completion_pct,
        "avg_rating": avg_rating,
        "avg_rating_stars": star_string,
    })

@role_required(['company'])
def supervisor_timesheets_calendar(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id)
    logs = OJTProgress.objects.filter(placement=placement)
    log_dates = {log.date for log in logs}
    logs_dict = {log.date: log for log in logs}

    MAX_HOURS = 600

    total_hours = logs.aggregate(total=Sum('hours_worked'))['total'] or 0
    completion_pct = round(total_hours / MAX_HOURS * 100, 1)

    avg_rating = logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0
    avg_rating = round(avg_rating, 2)

    # Generate stars
    def generate_stars(rating):
        stars = ""
        for i in range(1, 6):
            if rating >= i:
                stars += "★"
            else:
                stars += "☆"
        return stars

    avg_rating_stars = generate_stars(avg_rating)

    months = []
    for month_num in range(1, 7):
        cal = calendar.Calendar(firstweekday=6)
        month_days = list(cal.itermonthdates(2026, month_num))
        months.append({
            'name': calendar.month_name[month_num],
            'days': month_days,
            'number': month_num
        })

    return render(request, 'companies/supervisor-timesheets-calendar.html', {
        'placement': placement,
        'months': months,
        'log_dates': log_dates,
        'logs_dict': logs_dict,
        'total_hours': total_hours,
        'completion_pct': completion_pct,
        'avg_rating': avg_rating,
        'avg_rating_stars': avg_rating_stars,
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
