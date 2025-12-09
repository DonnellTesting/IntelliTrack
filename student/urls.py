from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='student_dashboard'),
    path('class/', views.student_class, name='student_class'),
    path('timesheets/<placement_id>', views.student_timesheets, name='student_timesheets'),
    path('timesheets/calendar/<int:placement_id>',views.student_timesheets_calendar,name='student_timesheets_calendar'),
    
    # Announcements
    path('announcements/', views.student_announcements, name='student_announcements'),
]
