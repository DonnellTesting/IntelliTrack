from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='student_dashboard'),
    path('timesheet/', views.student_timesheet, name='student_timesheet'),
    path('performance/', views.student_performance, name='student_performance'),
    path('placement/', views.student_placement, name='student_placement'),
    
    # Announcements
    path('announcements/', views.student_announcements, name='student_announcements'),
]
