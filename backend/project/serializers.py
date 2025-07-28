from rest_framework import serializers
from .models import Project
from team.models import Team

# Project’in tüm temel alanları için serializer
class ProjectSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)  # Takım ismini de kolay erişim için
    team_owner = serializers.CharField(source='team.owner', read_only=True)
    owner_id = serializers.IntegerField(source='team.owner.id', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'team', 'team_name','team_owner','owner_id', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
