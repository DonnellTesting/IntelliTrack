from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='supervisor_dashboard'),

    # Management
    path('students/', views.supervisor_students, name='supervisor_students'),
    path('timesheets/', views.supervisor_timesheets, name='supervisor_timesheets'),
    path('performance/', views.supervisor_performance, name='supervisor_performance'),

    # Announcements
    path('announcements/create/', views.supervisor_ann_create, name='supervisor_ann_create'),
    path('announcements/view/', views.supervisor_ann_view, name='supervisor_ann_view'),
]
