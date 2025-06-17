from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


router = DefaultRouter()
# Routers
router.register(r"register", views.UserRegistration, basename="register-user")

urlpatterns = [
    # obtain jwt access/refresh token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Email verification
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
    path(
        "resend-verfication-email/",
        views.ResendVerificationEmail.as_view(),
        name="resend-verification-email",
    ),
    # Router
    path("", include(router.urls)),
    # OTP setup
    path(
        "request-password-reset/",
        views.RequestOtp.as_view(),
        name="request-password-reset",
    ),
    path(
        "reset-password-with-otp/",
        views.ResetPasswordWithOtp.as_view(),
        name="reset-password-with-otp",
    ),
]
