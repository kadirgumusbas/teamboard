from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ?project=ID ile filtreleme, sadece kendi takımı/projesi taskleri için:
        project_id = self.request.query_params.get('project')
        team_id = self.request.query_params.get('team')
        my_tasks = self.request.query_params.get('my')
        queryset = Task.objects.all()
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if team_id:
            queryset = queryset.filter(project__team_id=team_id)
        if my_tasks:  # /api/tasks/?my=1
            queryset = queryset.filter(assignee=self.request.user)
        return queryset

    # Sadece kullanıcının atandığı taskler (aksiyonla):
    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Bir projenin tüm taskleri (aksiyonla):
    @action(detail=False, methods=['get'], url_path='by-project/(?P<project_id>[^/.]+)')
    def by_project(self, request, project_id=None):
        tasks = Task.objects.filter(project_id=project_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Bir takımın tüm taskleri:
    @action(detail=False, methods=['get'], url_path='by-team/(?P<team_id>[^/.]+)')
    def by_team(self, request, team_id=None):
        tasks = Task.objects.filter(project__team_id=team_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
