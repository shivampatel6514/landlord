from rest_framework import serializers
from .models import CustomUser,PropertyType,Property
from .models import Tag

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'role_type', 'mobile', 'address')
        extra_kwargs = {'password': {'write_only': True}}


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('id', 'name', 'tag', 'property_type', 'image', 'price','bedrooms','bathrooms','zipcode','description','address','features','nearest_station')