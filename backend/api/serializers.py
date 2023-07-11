import django.contrib.auth.password_validation as validator
from django.contrib.auth.hashers import make_password
from django.core import exceptions as django_exceptions
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Subscribe

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )


class GetUserSerializer(UserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribe'
        )

    def get_is_subscribe(self, obj):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):
            return Subscribe.objects.filter(user=self.context['request'].user,
                                            author=obj).exists()
        return False


# class ChangePasswordSerializer(serializers.Serializer):
#     current_password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(write_only=True)

#     def validate_current_password(self, current_password):
#         # print(self.instance)
#         username = self.instance
#         if not authenticate(
#                 username=username,
#                 password=current_password):
#             raise serializers.ValidationError(
#                 {'current_password': 'Неправильный текущий пароль.'}
#             )
#         return current_password

#     def validate_new_password(self, new_password):
#         validator.validate_password(new_password)
#         return new_password

#     def create(self, validated_data):
#         user = self.context['request'].user
#         password = make_password(
#             validated_data.get('new_password'))
#         user.password = password
#         user.save()
#         return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, new_password):
        validator.validate_password(new_password)
        return new_password

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError(
                {'current_password': 'Неправильный пароль.'}
            )
        if (validated_data['current_password']
           == validated_data['new_password']):
            raise serializers.ValidationError(
                {'new_password': 'Новый пароль должен отличаться от текущего.'}
            )
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


# class TokenSerializer(serializers.Serializer):
#     email = serializers.CharField(
#         label='Email',
#         write_only=True)
#     password = serializers.CharField(
#         label='Пароль',
#         write_only=True)

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         if email and password:
#             user = User.objects.get(email=email)
#             if not user:
#                 msg = 'Пользователь с указанными данными не найден'
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = 'Не указаны "электронная почта" или "пароль".'
#             raise serializers.ValidationError(msg)
#         attrs['user'] = user
#         return attrs
