from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        
        # if user.check_password(password):
        if check_password(password, user.password):

            return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
