from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsEmployerOrReadOnly
from .models import Job
from .serializers import JobSerializer
from .filters import JobFilter


class ManageJobs(viewsets.ModelViewSet):
    """
    ViewSet for managing job posts at `/api/jobs/panel/`.

    Employers can:
    - POST to create new job
    - PUT/PATCH to update
    - DELETE to remove

    Public users can:
    - GET a list of all jobs (with filters)
    - GET a specific job by ID

    🔍 Supported filters:
    - `title` — Filter by partial job title (case-insensitive)
    - `employment_type` — Filter by job type (e.g. FT, PT, etc.)
    - `min_salary` / `max_salary` — Salary range filtering

    Example:
    `/api/jobs/panel/?title=developer&min_salary=40000`
    """

    permission_classes = [IsEmployerOrReadOnly]
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = JobFilter
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "salary"]
