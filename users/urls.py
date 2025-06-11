from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


router = DefaultRouter()
# Routers
router.register(r"register", views.UserRegistration, basename="register-user")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
    path("", include(router.urls)),
]
