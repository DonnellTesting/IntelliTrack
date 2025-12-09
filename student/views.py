# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from student.models import OJTPlacement, OJTProgress
from accounts.models import Announcement
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from datetime import date
import calendar
from django.db.models import Sum, Avg

@role_required(['student'])
def dashboard(request):
    return render(request, 'student/student-dashboard.html')

@role_required(['student'])
def student_class(request):
    placements = (
        OJTPlacement.objects
        .select_related("student")
        .order_by("company_name", "student__last_name", "student__first_name")
    )

    return render(request, "student/student-class.html", {
        "placements": placements
    })

@role_required(['student'])
def student_timesheets(request, placement_id):
    placement = get_object_or_404(
        OJTPlacement,
        id=placement_id,
        student=request.user 
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

    return render(request, "student/student-timesheets.html", {
        "placement": placement,
        "logs": logs,
        "total_hours": total_hours,
        "completion_pct": completion_pct,
        "avg_rating": avg_rating,
        "avg_rating_stars": star_string,
    })

@role_required(['student'])
def student_timesheets_calendar(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id, student=request.user)
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

    return render(request, 'student/student-timesheets-calendar.html', {
        'placement': placement,
        'months': months,
        'log_dates': log_dates,
        'logs_dict': logs_dict,
        'total_hours': total_hours,
        'completion_pct': completion_pct,
        'avg_rating': avg_rating,
        'avg_rating_stars': avg_rating_stars,
    })

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