from rest_framework import serializers
from .models import User
from .utils import send_verification_email, delete_otp, get_otp


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles registration data validation and user creation.

    - Validates unique email and matching passwords
    - Saves a new inactive user instance
    - Triggers email verification flow after creation
    """

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
            raise serializers.ValidationError("This Email already exists")
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


class RequestOtpSerializer(serializers.Serializer):
    """
    Validates email input for password reset request.

    - Ensures user with the email exists
    - Triggers email with password reset token
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("User with this email does not exist.")
        if not user.is_active:
            raise serializers.ValidationError("Email not verified.")
        return value


class ResetPasswordWithOtpSerializer(serializers.Serializer):
    """
    Validates new password submission using reset token.

    - Accepts token and new password fields
    - Resets user's password after token validation
    """

    email = serializers.EmailField()
    otp = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    confirm_password = serializers.CharField(
        min_length=8, max_length=128, write_only=True
    )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password do not match")
        stored_otp = get_otp(attrs["email"])
        print("Stored OTP:", stored_otp)
        print("Entered OTP:", attrs["otp"])
        if not stored_otp or stored_otp != attrs["otp"]:
            raise serializers.ValidationError("Invalid or expired otp")

        return attrs

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        user.set_password(self.validated_data["password"])
        user.save()
        delete_otp(user.email)
