from accounts.models import User
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_repeat'):
            raise serializers.ValidationError(
                {
                    'detail': 'Password doesn\'t match with its repetition'
                }
            )

        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password_repeat')
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_repeat']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_repeat = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_repeat'):
            raise serializers.ValidationError(
                {
                    'detail': 'New password doesn\'t match with its repetition',
                }
            )

        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {
                    'new_password': list(e.messages),
                }
            )

        return super().validate(attrs)
