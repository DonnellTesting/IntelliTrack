from django.urls import path
from . import views

urlpatterns = [
    #Default Dash
    path('', views.dashboard, name='supervisor_dashboard'),

    # Management
    path('students/', views.supervisor_students, name='supervisor_students'),
    path('students/view/', views.supervisor_students_view, name='supervisor_students_view'),
    path('students/modify', views.supervisor_students_modify, name='supervisor_students_modify'),
    path('timesheets/modify/<placement_id>', views.supervisor_timesheets_modify, name='supervisor_timesheets_modify'),
    path('timesheets/view/<placement_id>', views.supervisor_timesheets_view, name='supervisor_timesheets_view'),
    path('timesheets/delete/<log_id>', views.supervisor_timesheets_delete, name='supervisor_timesheets_delete'),

    # Announcements
    path('announcements/create/', views.supervisor_ann_create, name='supervisor_ann_create'),
    path('announcements/view/', views.supervisor_ann_list, name='supervisor_ann_view'),
    path('announcements/delete/<int:pk>/', views.supervisor_ann_delete, name='supervisor_ann_delete'),
]
