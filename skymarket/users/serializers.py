from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()
# TODO Здесь нам придется переопределить сериалайзер, который использует djoser
# TODO для создания пользователя из за того, что у нас имеются нестандартные поля


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name',
                  'last_name',
                  'email',
                  'password',
                  'phone',
                  'image']


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name',
                  'last_name',
                  'email',
                  'phone',
                  'id',
                  'image']
