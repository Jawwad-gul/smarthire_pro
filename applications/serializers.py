from rest_framework import serializers
from .models import Application
from rest_framework.exceptions import ValidationError


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializes job application data.

    - Used by candidates to apply for jobs
    - Captures resume file, cover letter, and applied job reference
    - Read-only for employers viewing applications submitted to their jobs
    """

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("status", "applied_at", "candidate")

    def validate(self, attrs):
        user = self.context["request"].user
        job = attrs.get("job")
        if not user.is_authenticated or not user.is_candidate:
            raise ValidationError("User must be a authenticated & candidate")

        if Application.objects.filter(candidate=user, job=job).exists():
            raise ValidationError("You have already applied for this job..")

        if job.posted_by == user:
            raise ValidationError("Employer cant apply to his own job")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["candidate"] = user
        return super().create(validated_data)
