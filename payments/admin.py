from django.contrib import admin


from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_intent_id", "amount", "status", "created_at")
    search_fields = ("payment_intent_id", "user__email")
