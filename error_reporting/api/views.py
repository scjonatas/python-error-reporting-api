from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import views as jwt_views
from filters.mixins import FiltersMixin
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer, EventSerializer
from .validations import users_query_schema
from .models import Event


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Returns a token and a refresh token for valid credentials',
    operation_description="""
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.

    You can use the following credentials to test:
    ```
    {
        "username": "admin",
        "password": "admin"
    }
    ```
    """
))
class TokenObtainPairView(jwt_views.TokenObtainPairView):
    pass


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Returns a token if the refresh token is valid',
    operation_description="""
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
))
class TokenRefreshView(jwt_views.TokenRefreshView):
    pass

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Returns a list of Auth Users',
    operation_description=f"""
        You can filter the results by using the following parameters in the query string:
        ```
        username
        first_name
        last_name
        email
        date_joined
        date_joined__gt
        date_joined__lt
        date_joined__gte
        date_joined__lte
        last_login
        last_login__gt
        last_login__lt
        last_login__gte
        last_login__lte
        ```
    """
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Creates an Auth User'
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Find an Auth User by ID'
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Updates an Auth User'
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially updates an Auth User'
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Deletes an Auth User'
))
class UserViewSet(FiltersMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    filter_mappings = {
        "username": "username",
        "first_name": "first_name__icontains",
        "last_name": "last_name__icontains",
        "email": "email__icontains",
        "date_joined": "date_joined",
        "date_joined__gt": "date_joined__gt",
        "date_joined__lt": "date_joined__lt",
        "date_joined__gte": "date_joined__gte",
        "date_joined__lte": "date_joined__lte",
        "last_login": "last_login",
        "last_login__gt": "last_login__gt",
        "last_login__lt": "last_login__lt",
        "last_login__gte": "last_login__gte",
        "last_login__lte": "last_login__lte",
    }

    filter_validation_schema = users_query_schema

    def save_user(self, serializer):
        password = None
        if ('password' in self.request.data):
            # Encrypt password
            password = make_password(self.request.data['password'])
        serializer.save(password=password)

    def perform_create(self, serializer):
        self.save_user(serializer)

    def perform_update(self, serializer):
        self.save_user(serializer)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Returns a list of Events'
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Creates an Event'
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Find an Event by ID'
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Deletes an Event'
))
class EventViewSet(
    FiltersMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
