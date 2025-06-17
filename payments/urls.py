from django.urls import path, include
from . import views

urlpatterns = [
    path(
        "confirm-payment/", views.ConfirmPaymentView.as_view(), name="confirm-payment"
    ),
    path(
        "create-payment-intent/",
        views.CreatePaymentIntent.as_view(),
        name="create-payment-intent",
    ),
    path(
        "get-stripe-public-key/",
        views.GetStripePublicKey.as_view(),
        name="get-stripe-public-key",
    ),
]
