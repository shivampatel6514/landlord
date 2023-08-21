from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password  
from .serializers import CustomUserSerializer

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser    
from rest_framework.generics import get_object_or_404



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
                                'refresh_token': str(refresh),
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

@api_view(['GET'])
def index(request):
    return Response({"message": "hii"})