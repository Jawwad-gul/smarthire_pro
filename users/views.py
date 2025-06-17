from .serializers import (
    UserRegistrationSerializer,
    RequestOtpSerializer,
    ResetPasswordWithOtpSerializer,
)
from .models import User

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

# from rest_framework.throttling import UserRateThrottle

from .utils import (
    send_verification_email,
    send_password_reset_otp,
    generate_otp,
    store_otp,
)

import stripe


class UserRegistration(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Handles user registration.

    - `POST /api/auth/register/` – Register a new user (email/password)
    - Sends verification email with a token
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class VerifyEmail(APIView):
    """
    Verifies user's email using token from email link.

    - `GET /api/auth/verify-email/?token=...` – Activate the user's account
    """

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response(
                {"detail": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response(
                    {"detail": "This Email is already verified"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
            user.is_active = True
            user.save()
            return Response(
                {"detail": "Email successfully verified"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Error in verifying email token: {e}")
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendVerificationEmail(APIView):
    """
    Resends the verification email to the user.

    - `POST /api/auth/resend-verification/` – Request a new email verification link
    - Rate limited (e.g., once per minute)
    """

    # throttle_classes = [UserRateThrottle]

    def post(self, request):
        email_ = request.data.get("email")
        if not email_:
            return Response(
                {"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(email=email_)
            if user.is_active:
                return Response(
                    {"detail": "The Email has already been verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            send_verification_email(user)
            return Response(
                {"detail": "Verfication Email send"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "No user found with this Email"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RequestOtp(APIView):
    """
    Initiates password reset via email.

    - `POST /api/auth/password-reset/request/` – Sends reset token to email
    """

    def post(Self, request):
        serializer = RequestOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = generate_otp()
            store_otp(otp, email)
            send_password_reset_otp(email, otp)
            return Response(
                {"detail": "OTP send to your Email"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordWithOtp(APIView):
    """
    Resets password using token.

    - `POST /api/auth/password-reset/confirm/` – Confirms new password
    """

    def post(self, request):
        serializer = ResetPasswordWithOtpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
