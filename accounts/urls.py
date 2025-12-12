from django.urls import path
from .views import landing_page
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', landing_page, name='landing-page'),  # root of the app
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('signin/', views.login_page, name='signin'),  # same as login
    # path('forgot-password/', views.forgot_password, name='forgot_password'), #change to reset-password
    # path('reset-password/', views.reset_password, name='reset_password'), #change to reset-password-sent
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('timesheets/print/<int:placement_id>/', views.timesheets_print, name='timesheets_print'),
    path('timesheets/certificate/<int:placement_id>', views.timesheets_certificate, name='timesheets_certificate'),

    path("reset-password/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"
         ),
         name="password_reset"),

    path("reset-password/sent/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"
         ),
         name="password_reset_done"),

    path("reset-password/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html"
         ),
         name="password_reset_confirm"),

    path("reset-password/confirm/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_complete.html"
         ),
         name="password_reset_complete"),
]

