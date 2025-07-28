from rest_framework import serializers

from project.models import Project
from .models import Task
from user.models import CustomUser  # Eğer kullanmak istersen


class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    team_id = serializers.IntegerField(source='project.team.id', read_only=True)
    team_name = serializers.CharField(source='project.team.name', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)
    owner_id = serializers.IntegerField(source='project.team.owner.id', read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # writeable field


    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status','project', 'due_date','owner_id', 'created_at',
            'assignee', 'assignee_username',
            'project_id', 'project_title',
            'team_id', 'team_name'
        ]
        read_only_fields = ['id', 'created_at', 'assignee_username', 'project_title', 'project_id', 'team_id', 'team_name']

    def create(self, validated_data):
        print("VALIDATED DATA:", validated_data)
        return super().create(validated_data)