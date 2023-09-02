from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status,viewsets
from django.contrib.auth.hashers import make_password  
from .serializers import CustomUserSerializer,TagSerializer,PropertyTypeSerializer,PropertySerializer
import imghdr
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,Tag,PropertyType,Property    
from rest_framework.generics import get_object_or_404
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import json,re,os
import base64
from PIL import Image
from io import BytesIO

from django.http import FileResponse
from django.conf import settings

def catch_all(path):
    # Construct the absolute path to the requested file
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Check if the file exists and serve it if it does
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))

    # If the file doesn't exist, return a 404 response
    else:
        raise Http404("File not found")
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "success":True,
                    "message":"login successfully",
                    "data":
                            {
                                'name':user.name,
                                'email':user.email,
                                'role_type':user.role_type,
                                'access_token': str(refresh.access_token),
                                # 'refresh_token': str(refresh),
                            }
                }, status=status.HTTP_200_OK)
        else:
            return Response({"success":False,'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateUserAPIView(APIView):
    def post(self, request):
        data = request.data.copy()  # Create a copy of the request data
        password = data.pop('password', None)  # Remove the password from data and get it

        if password:
            data['password'] = make_password(password)  # Hash the password

        serializer = CustomUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User Created successfully",
                "data": serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):    
    def put(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)  # Get the user instance by user_id

        data = request.data.copy()
        password = data.pop('password', None)
        if password:
            data['password'] = make_password(password)

        serializer = CustomUserSerializer(user, data=data, partial=True)  # Use partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message": "User updated successfully.","data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":False,"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteUserAPIView(APIView):
    def delete(self, request, user_id):
        try:
            user = get_object_or_404(CustomUser, pk=user_id)  # Get the user instance by user_id
            user.delete()
            return Response({"success":True,"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except CustomUser.DoesNotExist:
            return Response({"success":False,"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"success":False,"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
class ListUserAPIView(APIView):
    def get(self, request):
        custom_users = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        return Response({"success":True,"message":"data get successfully","data":serializer.data}, status=status.HTTP_200_OK)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "success": True,
            "message": "Data retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Id not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        data = {
            "success": True,
            "message": "Data retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {
                "success": True,
                "message": "Data created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "success": False,
                "message": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Data not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            data = {
                "success": True,
                "message": "Data updated successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                "message": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Id not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        data = {
            "success": True,
            "message": "Data deleted successfully"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "success": True,
            "message": "Data retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Id not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        data = {
            "success": True,
            "message": "Data retrieved successfully",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {
                "success": True,
                "message": "Data created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "success": False,
                "message": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Data not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            data = {
                "success": True,
                "message": "Data updated successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "success": False,
                "message": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            data = {
                "success": False,
                "message": "Id not found"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        data = {
            "success": True,
            "message": "Data deleted successfully"
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def custom_response(self, success, message=None, data=None, status_code=status.HTTP_200_OK):
        response_data = {
            "success": success,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            encoded_images = request.data.get('images', [])
            self.perform_create(serializer)
            property_id = serializer.data['id']
            directory_path = f'property_images/{property_id}'
            os.makedirs(directory_path, exist_ok=True)

            decoded_images = []

            for index, encoded_image in enumerate(encoded_images):
                try:
                    image_data = base64.b64decode(encoded_image)
                    image_format = imghdr.what(None, image_data)

                    if image_format in ['jpeg', 'png']:
                        image_path = f'{directory_path}/image_{index + 1}.{image_format}'
                        with open(image_path, 'wb+') as destination:
                            destination.write(image_data)
                        decoded_images.append(image_path)
                except (base64.binascii.Error, TypeError, ValueError):
                    pass

            return self.custom_response(success=True,message='Data created successfully',
                data={
                    'property_id': property_id,
                    'decoded_images': decoded_images,
                },
                status_code=status.HTTP_201_CREATED
            )
        else:
            return self.custom_response(success=False,message=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        properties = Property.objects.all()
        serialized_properties = PropertySerializer(properties, many=True)

        # Create a dictionary to store property data with image URLs
        properties_with_image_urls = []

        for property_data in serialized_properties.data:
            property_id = property_data['id']
            image_urls = []

            # Assuming that property images are stored in a specific directory
            image_directory = f'property_images/{property_id}'

            # Check if the directory exists
            if os.path.exists(image_directory):
                for filename in os.listdir(image_directory):
                    # Assuming image files have a specific naming convention
                    if filename.startswith("image_") and filename.endswith((".jpeg", ".jpg", ".png")):
                        image_urls.append(f'{request.build_absolute_uri("/")}{image_directory}/{filename}')

            property_data['image_urls'] = image_urls
            properties_with_image_urls.append(property_data)

        return Response(properties_with_image_urls, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return self.custom_response(success=False, message="Id not found", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        # Assuming the serializer includes an 'image_url' field
        # that provides the URL to the image associated with the object
        response_data = {
            **serializer.data,
            'image_url': self.get_image_url(serializer.data)  # Implement this method to get the image URL
        }
        return self.custom_response(success=True, message="Data retrieved successfully", data=response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
        except Http404:
            return self.custom_response(success=False, message="Data not found", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            # Assuming the serializer includes an 'image_url' field
            # that provides the URL to the image associated with the updated object
            response_data = {
                **serializer.data,
                'image_url': self.get_image_url(serializer.data)  # Implement this method to get the image URL
            }
            return self.custom_response(success=True, message="Data updated successfully", data=response_data)
        else:
            return self.custom_response(success=False, message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return self.custom_response(success=False, message="Id not found", status_code=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)
        return self.custom_response(success=True, message="Data deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
# class PropertyTypeViewSet(viewsets.ModelViewSet):
#     queryset = PropertyType.objects.all()
#     serializer_class = PropertyTypeSerializer

# class PropertyViewSet(viewsets.ModelViewSet):
#     queryset = Property.objects.all()
#     serializer_class = PropertySerializer

@api_view(['GET'])
def index(request):
    return Response({"message": "hii"})