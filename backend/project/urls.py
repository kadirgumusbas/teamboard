from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MyTeamsWithProjects

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Tüm ProjectViewSet endpointleri (CRUD + custom action’lar)
    path('', include(router.urls)),

    # Kullanıcının üye/sahibi olduğu takımlar ve projeler (sol navbar için)
    path('my-teams-with-projects/', MyTeamsWithProjects.as_view(), name='my-teams-with-projects'),
]
