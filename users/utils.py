from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail


def get_email_verification_token(user):
    token = AccessToken.for_user(user)
    return str(token)


def send_verification_email(user):
    token = get_email_verification_token(user)

    verify_url = f"{settings.FRONTEND_URL}/auth/verify-email/?token={token}"

    subject = "PLease verify your email"
    message = f"Hello {user.first_name}, You are verifying your email for Smarthire_Pro. Please click on the link below to verify your email\n\n{verify_url}\n\n Please ignore this if you didn't request for this."

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
