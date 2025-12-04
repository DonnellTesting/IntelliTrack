from django.urls import path
from .views import landing_page
from . import views

urlpatterns = [
    path('', landing_page, name='landing-page'),  # root of the app
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('signin/', views.login_page, name='signin'),  # same as login
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_user, name='logout'),
]
