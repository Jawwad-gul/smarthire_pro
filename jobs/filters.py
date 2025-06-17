import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    """
    Provides filtering options for job listings.

    🔍 Available Filters:

    - `title`: Filter by job title (case-insensitive, partial match)
    - `employment_type`: Filter by job type (e.g., FT, PT, CT, FL, IN, RM)
    - `min_salary`: Return jobs with salary >= value
    - `max_salary`: Return jobs with salary <= value
    """

    min_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="gte")
    max_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="lte")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    employment_type = django_filters.CharFilter(
        field_name="employment_type", lookup_expr="exact"
    )

    class Meta:
        model = Job
        fields = ["title", "employment_type"]
