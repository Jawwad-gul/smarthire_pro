from django.shortcuts import render
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


class UserRegistration(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class VerifyEmail(APIView):
    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response(
                {"detail": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            user = User.objects.get(id=user_id)

            if user.is_active:
                return Response(
                    {"detail": "This Email is already verified"},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
            user.is_active = True
            user.save()
            return Response(
                {"detail": "Email successfully verified"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Error in verifying email token: {e}")
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
