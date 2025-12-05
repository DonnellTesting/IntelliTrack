# student/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ojt_tracker.decorators import role_required

@role_required(['admin'])
def dashboard(request):
    return render(request, 'admin_panel/admin-dashboard.html')

# USER MGMT
@role_required(['admin'])
def admin_user_add(request):
    return render(request, "admin_panel/admin-users-add.html")

@role_required(['admin'])
def admin_user_edit(request):
    print("Hit1")
    return render(request, "admin_panel/admin-users-edit.html")

@role_required(['admin'])
def admin_user_delete(request):
    return render(request, "admin_panel/admin-users-delete.html")

# CLASS MGMT
@role_required(['admin'])
def admin_class_create(request):
    return render(request, "admin_panel/admin-class-create.html")

@role_required(['admin'])
def admin_class_edit(request):
    return render(request, "admin_panel/admin-class-edit.html")

@role_required(['admin'])
def admin_class_delete(request):
    return render(request, "admin_panel/admin-class-delete.html")

# OJT MGMT
@role_required(['admin'])
def admin_ojt_placements(request):
    return render(request, "admin_panel/admin-ojt-placements.html")

