from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_employer",
        "is_candidate",
        "is_admin",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_employer",
                    "is_candidate",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_employer",
                    "is_candidate",
                ),
            },
        ),
    )
    search_fields = ("email",)


admin.site.register(User, UserAdmin)
from django.core.mail import send_mail

send_mail(
    subject="Test Email",
    message="If you see this, email works.",
    from_email="jawwadgul12@gmail.com",  # should match EMAIL_HOST_USER
    recipient_list=["jugaraccnt@gmail.com"],  # use your own or secondary
    fail_silently=False,
)
