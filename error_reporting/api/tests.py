import pytest
import uuid
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import EventUser


USER_PASSWORD = 'strong-test-pass'


# ----- FIXTURES -----
@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        kwargs['password'] = USER_PASSWORD
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_superuser(db, create_user):
    def make_superuser(**kwargs):
        default_args = {"is_staff": True, "is_superuser": True}
        return create_user(**{**kwargs, **default_args})
    return make_superuser


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_superuser, api_client):
    user = create_superuser(username='admin')
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


# ----- API TESTS -----
@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('user-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client_with_credentials):
    url = reverse('user-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, status_code', [
       ('', '', 400),
       ('', USER_PASSWORD, 400),
       ('admin', '', 400),
       ('admin', 'invalid_pass', 401),
       ('admin', USER_PASSWORD, 200),
    ]
)
def test_api_token_endpoint(
    username, password, status_code, create_user, api_client
):
    create_user(username='admin')
    url = reverse('api-token')
    data = {
        "username": username,
        "password": password
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, email, status_code', [
       ('', '', '', 400),
       ('', 'password', '', 400),
       ('', '', 'email@email.com', 400),
       ('username', '', '', 400),
       ('username', 'password', 'invalidemail@', 400),
       ('username', 'password', 'email@email.com', 201),
    ]
)
def test_api_post_user_validations(
    username, password, email, status_code, api_client_with_credentials
):
    url = reverse('user-list')
    data = {
        "username": username,
        "password": password,
        "email": email
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == status_code


# ----- MODEL TESTS -----
@pytest.mark.parametrize(
    'username, email, expected_success', [
       ('', '', False),
       ('', 'invalid-email@', False),
       ('', 'valid-email@email.com', True),
       ('username', '', True),
    ]
)
def test_event_user_validations(username, email, expected_success):
    success = True
    eventUser = EventUser()
    eventUser.username = username
    eventUser.email = email
    try:
        eventUser.full_clean()
    except ValidationError:
        success = False

    assert success == expected_success


@pytest.mark.django_db
@pytest.mark.parametrize(
    'data, status_code', [
       (
            {
                "level": "error",
                "message": "Error test"
            },
            400
       ),
       (
            {
                "agent": {
                    "event_user": {
                        "username": "test-user-event"
                    },
                    "name": "Chrome",
                    "version": "10"
                },
                "level": "error",
                "message": "Error test"
            },
            400
       ),
       (
            {
                "agent": {
                    "event_user": {
                        "username": "test-user-event"
                    },
                    "environment": "sandbox",
                    "version": "10"
                },
                "level": "error",
                "message": "Error test"
            },
            400
       ),
       (
            {
                "agent": {
                    "event_user": {
                        "username": "test-user-event"
                    },
                    "environment": "sandbox",
                    "name": "Chrome"
                },
                "level": "error",
                "message": "Error test"
            },
            400
       ),
       (
            {
                "agent": {
                    "event_user": {
                        "username": "test-user-event"
                    },
                    "environment": "sandbox",
                    "name": "Chrome",
                    "version": "10",
                    "address": "10.10.10"
                },
                "level": "error",
                "message": "Error test"
            },
            400
       ),
       (
            {
                "agent": {
                    "event_user": {
                        "username": "test-user-event"
                    },
                    "environment": "sandbox",
                    "name": "Chrome",
                    "version": "10",
                    "address": "192.168.0.2"
                },
                "level": "error",
                "message": "Error test"
            },
            201
       ),
       (
            {
                "agent": {
                    "environment": "sandbox",
                    "name": "Chrome",
                    "version": "10"
                },
                "level": "error",
                "message": "Error test"
            },
            201
       ),
    ]
)
def test_api_post_event(data, status_code, api_client_with_credentials):
    url = reverse('event-list')
    response = api_client_with_credentials.post(url, data=data, format='json')
    assert response.status_code == status_code
