"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user.views import UserRegistrationView, UserProfileView, UserProfileUpdateView, UserListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
]

# USER PROCESS
urlpatterns += [
                   path('register/', UserRegistrationView.as_view(), name='register'),
                   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                   path('profile/', UserProfileView.as_view(), name='user-profile'),
                   path('update-profile', UserProfileUpdateView.as_view(), name='user-profile-update'),
                   path('users/', UserListAPIView.as_view(), name='user-list'),
                   path('api/', include('team.urls')),
                   path('api/', include('project.urls')),
                    path('api/', include('task.urls')),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
