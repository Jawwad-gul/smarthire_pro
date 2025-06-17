from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"panel", views.ManageJobs, basename="job-panel")

urlpatterns = [
    path("", include(router.urls)),
]
