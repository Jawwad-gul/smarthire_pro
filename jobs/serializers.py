from rest_framework import serializers
from .models import Job
from rest_framework.validators import ValidationError


class JobSerializer(serializers.ModelSerializer):
    """
    Serializes Job model instances.

    - Used by employers to create, retrieve, or update job posts
    - Includes fields like title, description, salary, and employment type
    - Supports read/write operations for job listings
    """

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "posted_by")

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.is_authenticated or not user.is_employer:
            raise ValidationError("Only Emplpoyers can post a job")
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        return Job.objects.create(posted_by=user, **validated_data)
