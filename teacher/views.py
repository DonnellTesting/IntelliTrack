# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required
from .models import Class
from student.models import OJTPlacement, OJTProgress
from accounts.models import Announcement
from accounts.forms import AnnouncementForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from datetime import date
import calendar
from django.db.models import Sum, Avg

# Dashboard
@role_required(['instructor'])
def dashboard(request):
    students = OJTPlacement.objects.all()
    total_students = students.count()
    MAX_HOURS = 600

    total_hours = OJTProgress.objects.all().aggregate(total=Sum('hours_worked'))['total'] or 0
    class_completion_pct = (
        round(total_hours / (total_students * MAX_HOURS) * 100, 1)
        if total_students else 0
    )

    avg_rating = OJTProgress.objects.all().aggregate(avg=Avg('performance_rating'))['avg'] or 0

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

    # -------------------------
    # BUILD STUDENT DATA
    # -------------------------
    student_data = []
    for student in students:
        progress_logs = student.progress_logs.all()
        student_hours = progress_logs.aggregate(total=Sum('hours_worked'))['total'] or 0
        student_avg_rating = progress_logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0

        completion_pct = round(student_hours / MAX_HOURS * 100, 1)

        student_data.append({
            'name': student.student.get_full_name(),
            'initials': student.student.get_full_name().split()[0][0],
            'hours': student_hours,
            'completion_pct': completion_pct,
            'completion_remaining': round(100 - completion_pct, 1),
            'avg_rating': round(student_avg_rating, 2),
            'avg_rating_stars': generate_stars(student_avg_rating),
        })

    # 1. Rank by attendance (completion_pct)
    attendance_sorted = sorted(student_data, key=lambda s: s['completion_pct'], reverse=True)
    for rank, student in enumerate(attendance_sorted, start=1):
        student['attendance_rank'] = rank

    # 2. Rank by rating
    rating_sorted = sorted(student_data, key=lambda s: s['avg_rating'], reverse=True)
    for rank, student in enumerate(rating_sorted, start=1):
        student['rating_rank'] = rank

    # 3. Combined score (lower is better)
    for student in student_data:
        student['score'] = student['attendance_rank'] + student['rating_rank']

    # 4. Determine winners
    min_score = min(s['score'] for s in student_data)
    for student in student_data:
        student['is_top'] = (student['score'] == min_score)

    context = {
        'total_students': total_students,
        'class_completion_pct': class_completion_pct,
        'class_completion_remaining': 100 - class_completion_pct,
        'avg_rating': round(avg_rating, 2),
        'avg_rating_stars': avg_rating_stars,
        'student_data': student_data,
    }

    return render(request, 'teacher/teacher-dashboard.html', context)

#Class List
@role_required(['instructor'])   # Only company supervisors can access
def instructor_placements(request):

    # Get all students supervised by this logged-in company supervisor
    placements = OJTPlacement.objects.all().order_by("student__last_name", "student__first_name")

    return render(request, "teacher/teacher-class.html", {
        "placements": placements
    })

@role_required(['instructor'])   # Dash View
def instructor_timesheets(request):

    # Get all students supervised by this logged-in company supervisor
    placements = OJTPlacement.objects.all().order_by("student__last_name", "student__first_name")

    return render(request, "teacher/teacher-timesheets.html", {
        "placements": placements
    })

@role_required(['instructor'])
def instructor_timesheets_view(request, placement_id):
    placement = get_object_or_404(
        OJTPlacement,
        id=placement_id,
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

    return render(request, "teacher/teacher-timesheets-view.html", {
        "placement": placement,
        "logs": logs,
        "total_hours": total_hours,
        "completion_pct": completion_pct,
        "avg_rating": avg_rating,
        "avg_rating_stars": star_string,
    })

@role_required(['instructor'])
def instructor_timesheets_calendar(request, placement_id):
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

    return render(request, 'teacher/teacher-timesheets-calendar.html', {
        'placement': placement,
        'months': months,
        'log_dates': log_dates,
        'logs_dict': logs_dict,
        'total_hours': total_hours,
        'completion_pct': completion_pct,
        'avg_rating': avg_rating,
        'avg_rating_stars': avg_rating_stars,
    })

@role_required(['instructor'])
def instructor_timesheets_print(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id)
    logs = placement.progress_logs.all()

    MAX_HOURS = 600

    total_hours = logs.aggregate(total=Sum('hours_worked'))['total'] or 0
    completion_pct = round(total_hours / MAX_HOURS * 100, 1)

    avg_rating = logs.aggregate(avg=Avg('performance_rating'))['avg'] or 0
    avg_rating = round(avg_rating, 2)

    def generate_stars(rating):
        stars = ""
        for i in range(1, 6):
            stars += "★" if rating >= i else "☆"
        return stars

    star_string = generate_stars(avg_rating)

    today = date.today()

    return render(request, "teacher/teacher-timesheets-print.html", {
        "placement": placement,
        "logs": logs,
        "total_hours": total_hours,
        "completion_pct": completion_pct,
        "avg_rating": avg_rating,
        "avg_rating_stars": star_string,
        "today": today,
    })

@role_required(['instructor'])
def instructor_timesheets_certificate(request, placement_id):
    placement = get_object_or_404(OJTPlacement, id=placement_id)

    from datetime import date
    today = date.today()

    return render(request, "teacher/teacher-timesheets-certificate.html", {
        "placement": placement,
        "today": today,
    })

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
