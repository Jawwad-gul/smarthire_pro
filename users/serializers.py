from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_employer",
            "is_candidate",
            "password",
        ]

    def validate(self, attrs):
        if not attrs.get("is_candidate") and not attrs.get("is_employer"):
            raise serializers.ValidationError(
                "User must be either employer or candidate"
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
