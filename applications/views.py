from rest_framework import viewsets, mixins
from .permissions import IsCandidateOrReadOnly
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationView(viewsets.ModelViewSet):
    """
    ViewSet for job applications at `/api/applications/panel/`.

    - `GET  /api/applications/panel/`      – List applications
    - `POST /api/applications/panel/`      – Apply to a job
    - `GET  /api/applications/panel/{id}/` – View application details
    """

    permission_classes = [IsCandidateOrReadOnly]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_candidate:
            return Application.objects.filter(candidate=user)
        elif user.is_authenticated and user.is_employer:
            return Application.objects.filter(jobs__posted_by=user)
        return Application.objects.none()
