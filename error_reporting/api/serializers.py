from django.contrib.auth.models import User
from django.db.transaction import atomic
from rest_framework import serializers

from .models import Event, Agent, Environment, EventUser


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
        fields = ['id', 'url', 'username', 'password', 'first_name',
                        'last_name', 'email', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = '__all__'
        read_only_fields = ['id']


class AgentSerializer(serializers.ModelSerializer):
    environment = CreatableSlugRelatedField(
        slug_field='name', queryset=Environment.objects.all())
    event_user = EventUserSerializer(required=False)

    class Meta:
        model = Agent
        fields = '__all__'
        read_only_fields = ['id']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="event-detail")
    id = serializers.IntegerField(read_only=True)
    agent = AgentSerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def get_or_create_event_user(self, attributes: dict) -> 'EventUser':
        try:
            event_user = EventUser.objects.get(**attributes)
        except EventUser.DoesNotExist:
            event_user = EventUser(**attributes)
            event_user.full_clean()
            event_user.save()
        return event_user

    def get_or_create_agent(self, attributes: dict) -> 'Agent':
        try:
            agent = Agent.objects.get(**attributes)
        except Agent.DoesNotExist:
            agent = Agent(**attributes)
            agent.full_clean()
            agent.save()
        return agent

    @atomic
    def create(self, validated_data):
        agent_data = validated_data.pop('agent')

        if ('event_user' in agent_data):
            agent_data.event_user = self.get_or_create_event_user(
                agent_data.pop('event_user')
            )

        event = Event(**validated_data)
        event.agent = self.get_or_create_agent(agent_data)
        event.full_clean()
        event.save()
        return event
