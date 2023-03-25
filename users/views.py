import rest_framework.permissions
from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.permissions import *
from .serializer import *
from django.contrib.auth.views import PasswordResetConfirmView
# Create your views here.

class RegisterAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer


class UserIdentityAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserIdentity

    def get_object(self):
        return self.request.user

class ChangePasswordAPIView(UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = '/users/login'
