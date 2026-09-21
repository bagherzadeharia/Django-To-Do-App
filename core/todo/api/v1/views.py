from typing import override
from todo.models import Task
from rest_framework.status import *
from todo.api.v1.permissions import IsOwner
from rest_framework.response import Response
from rest_framework.decorators import action
from todo.api.v1.paginations import TaskPagination
from todo.api.v1.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

class TaskModelViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend]
    ordering_fields = ['updated_date']
    filterset_fields = ['title', 'complete']

    pagination_class = TaskPagination

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(
            self.filter_queryset(
                self.get_queryset()
            )
        )
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

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
            return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
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