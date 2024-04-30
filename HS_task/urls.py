"""
URL configuration for HS_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from django.contrib.auth import views as authViews

from users import views


router = routers.DefaultRouter()
router.register(r'users', views.InviteCode, basename='invitecodes')

urlpatterns = [
    path('', views.Homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('api/', views.InviteCode, name='inviteCode'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('cabinet', views.Cabinet, name='cabinet'),
    path('logout/', authViews.LogoutView.as_view(next_page='homepage'), name='logout'),
]
