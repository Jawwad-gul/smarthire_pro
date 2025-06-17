from django.db import models
from django.conf import settings


class Job(models.Model):
    EMPLOYMENT_TYPE = [
        ("FT", "Full-Time"),
        ("PT", "Part-Time"),
        ("CT", "Contract"),
        ("FL", "Freelance"),
        ("IN", "Internship"),
        ("RM", "Remote"),
    ]

    title = models.CharField(max_length=225)
    description = models.TextField()
    salary = models.PositiveIntegerField(null=True, blank=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE)
    is_premium = models.BooleanField(default=False)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
