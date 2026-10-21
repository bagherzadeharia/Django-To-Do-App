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
        response = api_client.put(url, {'title': 'hacked'})

        assert response.status_code == 403
        user_two_task.refresh_from_db()
        assert user_two_task.title == 'test'

    def test_get_own_task_detail_response_code_200(self, api_client, user_one):
        task = Task.objects.create(
            title='own task',
            complete=False,
            user=user_one,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': task.id})
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data['title'] == 'own task'
        assert response.data['complete'] is False

    def test_get_task_detail_forbidden_response_code_403(self, api_client, user_one, user_two):
        user_two_task = Task.objects.create(
            title='private task',
            complete=False,
            user=user_two,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': user_two_task.id})
        response = api_client.get(url)

        assert response.status_code == 403

    def test_update_own_task_response_code_200(self, api_client, user_one):
        task = Task.objects.create(
            title='old title',
            complete=False,
            user=user_one,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': task.id})
        response = api_client.put(url, {'title': 'new title', 'complete': True})

        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == 'new title'
        assert task.complete is True

    def test_delete_own_task_response_code_204(self, api_client, user_one):
        task = Task.objects.create(
            title='to delete',
            complete=False,
            user=user_one,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': task.id})
        response = api_client.delete(url)

        assert response.status_code == 204
        assert not Task.objects.filter(pk=task.id).exists()

    def test_delete_task_forbidden_response_code_403(self, api_client, user_one, user_two):
        user_two_task = Task.objects.create(
            title='keep this',
            complete=False,
            user=user_two,
        )
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-detail', kwargs={'pk': user_two_task.id})
        response = api_client.delete(url)

        assert response.status_code == 403
        assert Task.objects.filter(pk=user_two_task.id).exists()

    def test_create_task_without_title_response_code_400(self, api_client, user_one):
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-list')
        response = api_client.post(url, {'complete': False})

        assert response.status_code == 400
        assert Task.objects.filter(user=user_one).count() == 0

    def test_task_list_excludes_other_users_tasks(self, api_client, user_one, user_two):
        Task.objects.create(title='mine', complete=False, user=user_one)
        Task.objects.create(title='theirs', complete=False, user=user_two)
        api_client.force_authenticate(user=user_one)
        url = reverse('todo:api-v1:task-list')
        response = api_client.get(url)

        assert response.status_code == 200
        titles = [task['title'] for task in response.data['results']]
        assert 'mine' in titles
        assert 'theirs' not in titles
