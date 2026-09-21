from typing import override
from todo.models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_absolute_url', read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.full_name
        return representation

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    class Meta:
        model = Task
        fields = ['id', 'title', 'user', 'complete', 'created_date', 'updated_date', 'relative_url', 'absolute_url']
        read_only_fields = ['id', 'user', 'created_date']