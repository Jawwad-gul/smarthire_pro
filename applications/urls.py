from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"panel", views.ApplicationView, basename="application-panel")

urlpatterns = [path("", include(router.urls))]
