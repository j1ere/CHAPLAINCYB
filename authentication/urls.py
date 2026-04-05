# authenication/urls.py
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, ForgotPasswordView, ResetPasswordView , CSRFTokenView , AdminLoginView, VerifyEmailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("adminlogin/",AdminLoginView.as_view(), name='adminlogin'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("csrf/", CSRFTokenView.as_view()),
    path("profile/", ProfileView.as_view(), name="profile"),
    
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),

]