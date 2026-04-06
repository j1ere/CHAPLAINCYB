# authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User
from django.contrib.auth import login, authenticate, logout

from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


from django.shortcuts import redirect

from resend import Resend
import os

resend = Resend(api_key=os.getenv("RESEND_API_KEY"))


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            self.send_verification_email(request, user)

            return Response({
                "message": "Account created successfully. Please check your email to verify your account."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Use your real frontend domain in production
        # verification_link = f"https://stanneschaplaincy.com/verify-email/{uid}/{token}/"   # ← Change this!
        verification_link = f"https://api.stanneschaplaincy.com/auth/verify-email/{uid}/{token}/"# Change in production

        subject = "Verify your St. Anne's Chaplaincy Account"

        try:
            resend.emails.send(
                from_email="contact@contact.stanneschaplaincy.com",
                to=[user.email],
                subject=subject,
                html=f"""
                    <p>Hi {user.full_name or user.get_full_name() or user.email},</p>
                    <p>Thank you for registering with St. Anne's Chaplaincy at Maseno University.</p>
                    <p>Please click the link below to verify your email address and activate your account:</p>
                    <p><a href="{verification_link}">{verification_link}</a></p>
                    <p>This link will expire in 24 hours. If you did not register for an account, please ignore this email.</p>
                    <p>Best regards,<br>St. Anne's Chaplaincy ICT Team</p>
                """,
            )
            print(f"Verification email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send verification email to {user.email}: {e}")


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid verification link"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Automatically log the user in
            login(request, user)

            # return Response({
            #     "message": "Email verified successfully. You are now logged in."
            # }, status=200)
            return redirect("https://stanneschaplaincy.com/?verified=true")

        return Response({"error": "Invalid or expired token"}, status=400)




class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # if not (user.is_staff or user.is_superuser):
            #     return Response(
            #         {"error":"admin privilages required"},
            #         status=403
            #     )
            login(request, user)  # sets session cookie
            return Response({"message": "Logged in"})
        return Response({"error": "Invalid credentials"}, status=401)

class AdminLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if not (user.is_staff or user.is_superuser):
                return Response(
                    {"error":"admin privilages required"},
                    status=403
                )
            login(request, user)  # sets session cookie
            return Response({"message": "Logged in"})
        return Response({"error": "Invalid credentials"}, status=401)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})






@method_decorator(ensure_csrf_cookie, name="dispatch")
class CSRFTokenView(APIView):
    def get(self, request):
        return Response({
            "csrfToken": get_token(request)
        })




from django.contrib.auth import get_user_model

User = get_user_model()

# ==================== Forgot Password ====================

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # We still return success to prevent email enumeration
            return Response({
                "message": "If an account with this email exists, a password reset link has been sent."
            }, status=status.HTTP_200_OK)

        # Generate reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"https://stanneschaplaincy.com/reset-password/{uid}/{token}/"   

        subject = "Reset Your St. Anne's Chaplaincy Password"
        try:
            resend.emails.send(
                from_email="contact@contact.stanneschaplaincy.com",
                to=[user.email],
                subject=subject,
                html=f"""
                    <p>Hi {user.full_name or user.email},</p>
                    <p>You requested to reset your password for your St. Anne's Chaplaincy account.</p>
                    <p>Click the link below to reset your password:</p>
                    <p><a href="{reset_link}">{reset_link}</a></p>
                    <p>This link will expire in 24 hours. If you did not request a password reset, please ignore this email.</p>
                    <p>Best regards,<br>St. Anne's Chaplaincy Team</p>
                """,
            )
        except Exception as e:
            print(f"Password reset email failed: {e}")

        return Response({
            "message": "If an account with this email exists, a password reset link has been sent."
        }, status=status.HTTP_200_OK)


# ==================== Reset Password ====================

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired reset link"}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response({
            "message": "Password reset successful. You can now login with your new password."
        }, status=status.HTTP_200_OK)


############################################
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)



