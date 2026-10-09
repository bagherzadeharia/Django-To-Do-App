from accounts.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError(
                {
                    'detail': 'Passwords do not match'
                }
            )

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1')
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']
        extra_kwargs = {
            'password': {'write_only': True}
        }
