import pytest
from django.urls import reverse
from django.utils.timezone import now
from rest_framework.test import APIClient
from jsonschema.validators import RefResolver

from todo.models import Task
from accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_one():
    return User.objects.create_user(
        email="test_user_one@todo.app",
        password="Test@Password22",
        is_verified=True,
    )

@pytest.fixture
def user_two():
    return User.objects.create_user(
        email="test_user_two@todo.app",
        password="Test@Password22",
        is_verified=True,
    )

@pytest.mark.django_db
class TestToDoAPI:
    def test_get_task_list_response_code_200(self, api_client, user_one):
        user = user_one
        url = reverse('todo:api-v1:task-list')
        api_client.force_authenticate(user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_code_201(self, api_client, user_one):
        user = user_one
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

    def test_get_task_list_response_code_401(self, api_client):
        url = reverse('todo:api-v1:task-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_task_edit_forbidden_response_code_403(self, api_client, user_one, user_two):
        user_two_task = Task.objects.create(
            title='test',
            complete=False,
            user=user_two,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': user_two_task.id})
        response = api_client.patch(url, {'title': 'hacked'})

        assert response.status_code == 403
        user_two_task.refresh_from_db()
        assert user_two_task.title == 'test'
