from rest_framework import serializers
from .models import User
from .utils import send_verification_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_employer",
            "is_candidate",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if not attrs.get("is_candidate") and not attrs.get("is_employer"):
            raise serializers.ValidationError(
                "User must be either employer or candidate"
            )

        if attrs.get("is_candidate") and attrs.get("is_employer"):
            raise serializers.ValidationError(
                "User cannot be employer and candidate at the same time"
            )

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords are not same")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return serializers.ValidationError("This Email already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        send_verification_email(user)

        return user
