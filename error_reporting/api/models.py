from django.core.validators import EmailValidator, validate_ipv46_address
from django.db import models
from django_hint import StandardModelType

LEVEL_CHOICES = [
    ('fatal', 'Fatal'),
    ('debug', 'Debug'),
    ('error', 'Error'),
    ('warning', 'Warning'),
    ('info', 'Info'),
]


class EventUser(models.Model, StandardModelType):
    name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(validators=[EmailValidator], null=True)
    custom_data = models.TextField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['name']


class Environment(models.Model, StandardModelType):
    name = models.CharField(max_length=50)


class Agent(models.Model, StandardModelType):
    event_user = models.ForeignKey(EventUser, related_name='agent', on_delete=models.PROTECT, null=True)
    environment = models.ForeignKey(Environment, related_name='agent', on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    address = models.GenericIPAddressField(validators=[validate_ipv46_address], null=True)
    version = models.CharField(max_length=10)
    custom_data = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model, StandardModelType):
    agent = models.OneToOneField(Agent, on_delete=models.PROTECT)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.CharField(max_length=255)
    stacktrace = models.TextField(null=True)
    custom_data = models.TextField(null=True)
    archived = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.level + ' in ' + self.agent.name
