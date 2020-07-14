from django.contrib.auth.models import User
from rest_framework import serializers


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail('invalid')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']
