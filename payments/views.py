from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Payment
from .serializers import PaymentSerializer

from django.conf import settings

import stripe
import stripe.error

stripe.api_key = settings.STRIPE_SECRET_KEY


class ConfirmPaymentView(APIView):
    """
    Confirms a Stripe payment by verifying its PaymentIntent.

    - `POST /api/payments/confirm-payment/` – Retrieves the PaymentIntent and records its status in your DB
    """

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        payment_intent_id = request.data.get("payment_intent_id")
        if not payment_intent_id:
            return Response(
                {"detail": "Payment intent id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            payment, create = Payment.objects.update_or_create(
                payment_intent_id=payment_intent_id,
                defaults={
                    "user": request.user,
                    "amount": int(intent.amount) / 100,
                    "currency": intent.currency,
                    "status": intent.status,
                },
            )
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class CreatePaymentIntent(APIView):
    """
    Initiates a Stripe one-time payment session.

    - `POST /api/payments/create-payment-intent/` – Creates a new PaymentIntent and returns its client secret
    """

    def post(self, request):
        amount = request.data.get("amount")
        if not amount:
            return Response(
                {"detail": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )
            return Response(
                {"client_secret": intent.client_secret}, status=status.HTTP_200_OK
            )
        except intent.error.StripeError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetStripePublicKey(APIView):
    """
    Returns your Stripe publishable key.

    - `GET /api/payments/get-stripe-public-key/` – Fetch Stripe_PUBLISHABLE_KEY for client-side checkout
    """

    def get(self, request):
        try:
            return Response(
                {"stripe_public_key": settings.STRIPE_PUBLISHABLE_KEY},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
