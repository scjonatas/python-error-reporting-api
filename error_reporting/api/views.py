from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from filters.mixins import FiltersMixin

from .serializers import UserSerializer
from .validations import users_query_schema


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
