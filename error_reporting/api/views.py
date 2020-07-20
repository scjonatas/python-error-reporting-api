from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import views as jwt_views
from filters.mixins import FiltersMixin
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer, EventSerializer
from .validations import users_query_schema, events_query_schema
from .models import Event
from .docs import ResponseDocs


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
    """,
    responses={
        200: ResponseDocs.TOKEN_OK,
        400: ResponseDocs.TOKEN_BAD_REQUEST,
        401: ResponseDocs.TOKEN_UNAUTHORIZED
    }
))
class TokenObtainPairView(jwt_views.TokenObtainPairView):
    pass


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Returns a token if the refresh token is valid',
    operation_description="""
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """,
    responses={
        200: ResponseDocs.TOKEN_REFRESH_OK,
        400: ResponseDocs.TOKEN_REFRESH_BAD_REQUEST,
        401: ResponseDocs.TOKEN_REFRESH_UNAUTHORIZED
    }
))
class TokenRefreshView(jwt_views.TokenRefreshView):
    pass


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='Returns a list of Auth Users',
    operation_description="""
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
    """,
    responses={
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.INVALID_PAGE
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Creates an Auth User',
    responses={
        400: ResponseDocs.USER_BAD_REQUEST,
        401: ResponseDocs.UNAUTHORIZED
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Find an Auth User by ID',
    responses={
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_summary='Updates an Auth User',
    responses={
        400: ResponseDocs.USER_BAD_REQUEST,
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_summary='Partially updates an Auth User',
    responses={
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Deletes an Auth User',
    responses={
        204: 'No Content',
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
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
    operation_summary='Returns a list of Events',
    responses={
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.INVALID_PAGE
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_summary='Creates an Event',
    responses={
        400: ResponseDocs.EVENT_BAD_REQUEST,
        401: ResponseDocs.UNAUTHORIZED
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_summary='Find an Event by ID',
    responses={
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_summary='Deletes an Event',
    responses={
        204: 'No Content',
        401: ResponseDocs.UNAUTHORIZED,
        404: ResponseDocs.NOT_FOUND
    }
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

    filter_mappings = {
        "event_user_id": "agent__event_user",
        "event_user_name": "agent__event_user__name__icontains",
        "event_user_username": "agent__event_user__username",
        "event_user_email": "agent__event_user__email__icontains",
        "event_user_custom_data": "agent__event_user__custom_data__icontains",
        "agent_id": "agent__id",
        "agent_name": "agent__name__icontains",
        "environment": "agent__environment__name",
        "agent_address": "agent__address__startswith",
        "agent_version": "agent__version",
        "agent_custom_data": "agent__custom_data__icontains",
        "level": "level",
        "level__in": "level__in",
        "message": "message__icontains",
        "stacktrace": "stacktrace__icontains",
        "custom_data": "custom_data__icontains",
        "archived": "archived",
        "datetime_created": "datetime_created",
        "datetime_created__gt": "datetime_created__gt",
        "datetime_created__lt": "datetime_created__lt",
        "datetime_created__gte": "datetime_created__gte",
        "datetime_created__lte": "datetime_created__lte",
    }

    filter_validation_schema = events_query_schema
