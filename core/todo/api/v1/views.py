from typing import override
from rest_framework import status
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.vary import vary_on_headers
from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from todo.models import Task
from todo.api.v1.permissions import IsOwner
from todo.api.v1.paginations import TaskPagination
from todo.api.v1.serializers import TaskSerializer

@method_decorator(vary_on_headers("Authorization"), name="list")
class TaskModelViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['updated_date']
    filterset_fields = ['title', 'complete']

    pagination_class = TaskPagination

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        )

    def invalidate_tasks_cache(self, user_id):
        cache.delete_pattern(f"tasks:list:{user_id}:*")

    def list(self, request, *args, **kwargs):
        key = f"tasks:list:{request.user.id}:{request.get_full_path()}"
        data = cache.get(key)
        print(data)
        if data is None:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(key, data, timeout=60)

        print(data)
        return Response(data)

    def update(self, request, *args, **kwargs):
        task = Task.objects.get(
            pk=kwargs['pk']
        )
        print(request.user, task.user)
        if request.user != task.user:
            return Response(
                data={"detail": "Access Denied"},
                status=HTTP_403_FORBIDDEN
            )
        else:
            self.invalidate_tasks_cache(request.user.id)
            return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        self.invalidate_tasks_cache(request.user.id)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(
            pk=kwargs['pk']
        )
        if request.user != task.user:
            return Response(
                data={"detail": "Access Denied"},
                status=HTTP_403_FORBIDDEN
            )
        else:
            self.invalidate_tasks_cache(request.user.id)
            return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        task = Task.objects.get(
            pk=kwargs['pk']
        )
        if request.user != task.user:
            return Response(
                data={"detail": "Access Denied"},
                status=HTTP_403_FORBIDDEN
            )
        else:
            return super().retrieve(request, *args, **kwargs)
