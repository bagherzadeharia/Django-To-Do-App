import pytest
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APIClient
from jsonschema.validators import RefResolver

from accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def base_user():
    return User.objects.create_user(
        email="test_user@todo.app",
        password="Test@Password22",
        is_verified=True,
    )

@pytest.mark.django_db
class TestToDoAPI:
    def test_get_task_list_response_code_200(self, api_client, base_user):
        user = base_user
        url = reverse('todo:api-v1:task-list')
        api_client.force_authenticate(user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_code_201(self, api_client, base_user):
        user = base_user
        url = reverse('todo:api-v1:task-list')
        api_client.force_authenticate(user)
        taskData = {
            'title': 'test',
            'complete': False,
            'user': user,
            'created_date': now(),
            'updated_date': now(),
        }
        response = api_client.post(url, taskData)
        assert response.status_code == 201
