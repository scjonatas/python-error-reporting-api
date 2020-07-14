"""error_reporting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from error_reporting.api import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users/?', views.UserViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api/token/?$', jwt_views.TokenObtainPairView.as_view(), name='api-token'),
    url(r'^api/token/refresh/?$', jwt_views.TokenRefreshView.as_view(), name='api-token-refresh'),
    url(r'^api/hello/?$', views.HelloView.as_view()),
]
