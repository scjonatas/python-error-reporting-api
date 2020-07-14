from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from error_reporting.api.serializers import UserSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

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
