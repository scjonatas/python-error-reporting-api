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
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .api import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users/?', views.UserViewSet)
router.register(r'events/?', views.EventViewSet)

# Defining a router for swagger, because the "drf-yasg" was generating wrong endpoint paths for the paths ending with '/?'
router_for_swagger = routers.DefaultRouter()
router_for_swagger.register(r'users', views.UserViewSet)
router_for_swagger.register(r'events', views.EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/token/?$', views.TokenObtainPairView.as_view(), name='api-token'),
    url(r'^api/token/refresh/?$', views.TokenRefreshView.as_view(), name='api-token-refresh'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Error Reporting API",
        default_version='v1',
        description="""
                    API intended to report exceptions that occur in your application.
                    The endpoints requires a JWT Token. You can use the username: 'admin' and password: 'admin' to get the authentication token through the /token endpoint.
                    Once you get the token, you should pass the header 'Authorization: Bearer <your-token-here>' in the 'Authorization' header. The token is valid during 5 minutes.
                    Note: the trailing slashes at the endpoints are optional.
                    """,
        contact=openapi.Contact(email="scjonatas@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[url(r'^api/', include(router_for_swagger.urls))] + urlpatterns
)

urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
