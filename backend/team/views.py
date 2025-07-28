from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Team
from .serializers import TeamListSerializer, TeamDetailSerializer
from django.shortcuts import get_object_or_404
from django.db import models



class IsAdminOrTeamMember(permissions.BasePermission):
    """
    Admin ise her şeyi görebilir, member ise sadece kendi takımlarını.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
        return obj.members.filter(id=request.user.id).exists() or obj.owner == request.user

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminOrTeamMember()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        # Sadece owner VEYA member olduğu takımlar, admin olsa da!
        return Team.objects.filter(
            models.Q(members=user) | models.Q(owner=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return TeamDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminOrTeamMember])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        # Owner tekrar eklenemez!
        if user_id == team.owner.id:
            return Response({'detail': 'Takım sahibi zaten daimî üyedir ve tekrar eklenemez.'}, status=400)
        user = get_object_or_404(get_user_model(), id=user_id)
        team.members.add(user)
        return Response({'status': 'member added'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAdminOrTeamMember])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        # Owner çıkarılamaz!
        if user_id == team.owner.id:
            return Response({'detail': 'Takım sahibi çıkarılamaz!'}, status=400)
        user = get_object_or_404(get_user_model(), id=user_id)
        team.members.remove(user)
        return Response({'status': 'member removed'})
