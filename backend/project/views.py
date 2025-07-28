from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from task.serializers import TaskSerializer
from .models import Project
from .serializers import ProjectSerializer
from team.models import Team
from django.db.models import Q
from rest_framework.views import APIView
from team.serializers import TeamListSerializer, UserSimpleSerializer
from django_filters.rest_framework import DjangoFilterBackend

class IsTeamOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    - Takım sahibi veya admin ise ekleme/düzenleme/silme yapılabilir.
    - Diğer herkes sadece okuma yapabilir.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
            return True
        team_id = request.data.get('team') or request.query_params.get('team')
        if not team_id:
            return False
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return False
        return team.owner == request.user

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
            return True
        return obj.team.owner == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Tüm CRUD işlemleri, filtreleme, takıma özel ve genel erişim, istatistik, arama gibi işlevler burada.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'team']
    search_fields = ['title', 'description', 'team__name']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        user = self.request.user
        qs = Project.objects.all()

        # Admin tüm projeleri görebilir, diğerleri sadece üye olduğu/sahibi olduğu takımların projelerini görür
        if not (user.is_superuser or getattr(user, 'role', None) == 'admin'):
            teams = Team.objects.filter(Q(owner=user) | Q(members=user)).distinct()
            qs = qs.filter(team__in=teams)
        return qs

    # 5. (Ekstra) Projeye ait tasklerin nested endpointi (dummy örnek)
    @action(detail=True, methods=['get'], url_path='tasks')
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()  # related_name='tasks' ise
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # 9. (Ekstra) Proje özet/istatistik endpointi
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        total = Project.objects.count()
        active = Project.objects.filter(is_active=True).count()
        inactive = Project.objects.filter(is_active=False).count()
        return Response({
            'total': total,
            'active': active,
            'inactive': inactive
        })

    @action(detail=True, methods=['get'], url_path='assignable-users')
    def assignable_users(self, request, pk=None):
        project = self.get_object()
        members = project.team.members.all()
        serializer = UserSimpleSerializer(members, many=True)
        return Response(serializer.data)



# 2. Üyesi/sahibi olunan tüm takımları ve projelerini nested olarak dönen özel endpoint
class MyTeamsWithProjects(APIView):
    """
    Sol menüde kullanılmak üzere; kullanıcının üye veya sahibi olduğu takımlar ve altındaki projeler nested döner.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        teams = Team.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        data = []
        for team in teams:
            team_data = TeamListSerializer(team).data
            # Sadece aktif projeler istersek: team.projects.filter(is_active=True)
            team_data['projects'] = ProjectSerializer(team.projects.all(), many=True).data
            data.append(team_data)
        return Response(data)
