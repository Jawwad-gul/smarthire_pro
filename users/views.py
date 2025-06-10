from django.shortcuts import render
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status


class UserRegistration(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
