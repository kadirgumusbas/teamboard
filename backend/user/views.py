from django.shortcuts import render
from rest_framework import generics, permissions

from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserUpdateSerializer
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Sadece giriş yapan kendi profilini görebilsin
        return self.request.user


class UserProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            }
            for user in users
        ]
        return Response(data)