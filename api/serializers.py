from rest_framework import serializers
from .models import CustomUser,PropertyType

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'role_type', 'mobile', 'address')
        extra_kwargs = {'password': {'write_only': True}}


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name']
