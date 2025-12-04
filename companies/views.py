# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required

@role_required(['company'])
def dashboard(request):
    return render(request, 'companies/supervisor-dashboard.html')