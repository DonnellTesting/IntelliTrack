from django.urls import path
from . import views

urlpatterns = [
    #Default Dash
    path('', views.dashboard, name='instructor_dashboard'),

    #Class List
    path('class/', views.instructor_class_list, name='instructor_class'),

    # OJT Management
    path('timesheets/', views.instructor_timesheets, name='instructor_timesheets'),
    path('performance/', views.instructor_performance, name='instructor_performance'),
    path('placements/', views.instructor_placements, name='instructor_placements'),

    # Announcements
    path('announcements/create/', views.instructor_announcement_create, name='instructor_announcement_create'),
    path('announcements/view/', views.instructor_announcement_list, name='instructor_announcement_list'),
]