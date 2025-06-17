from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail

# otp
from django.core.cache import cache
import random


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


# otp
def generate_otp():
    return str(random.randint(100000, 999999))


def store_otp(otp, email, time=600):
    cache.set(f"otp:{email}", otp, timeout=time)


def get_otp(email):
    return cache.get(f"otp:{email}")


def delete_otp(email):
    cache.delete(f"otp:{email}")


def send_password_reset_otp(email, otp):
    subject = "Your SmartHire password reset OTP"
    message = f"Your OTP is: {otp}, It will expire in 10 minutes"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject,
        message,
        from_email,
        [email],
    )
