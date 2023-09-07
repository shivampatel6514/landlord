from rest_framework import serializers
from .models import CustomUser,PropertyType,Property,Contact
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
    tag = TagSerializer()  # Use the custom TagSerializer for the tag field
    property_type = PropertyTypeSerializer()  # Use the custom PropertyTypeSerializer for the property_type field

    class Meta:
        model = Property
        fields = '__all__'
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'        