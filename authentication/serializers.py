from rest_framework import serializers, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from exceptions.custom_apiexception_class import *
User = get_user_model()


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password',
                  'first_name', 'last_name', 'phone_number', 'image', 'is_verified', 'is_social_user', 'is_business']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', "")
        password = data.get('password', "")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    return CustomAPIException(detail="Your account has been suspended", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

            else:
                return CustomAPIException(detail="Please check your credentials and try again!", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

        else:
            return CustomAPIException(detail="Please enter both username and password to login!", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class UserBusinessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category_type = BusinessCategorySerializer(many=True, read_only=False)

    class Meta:
        model = UserBusiness
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']

    def create(self, validated_data):
        category_type_data = validated_data.pop('category_type', [])
        user_business = UserBusiness.objects.create(**validated_data)
        user_business.category_type.set(category_type_data)
        return user_business

    def update(self, instance, validated_data):
        category_type_data = validated_data.pop('category_type', None)
        if category_type_data:
            instance.category_type.set(category_type_data)
        return super().update(instance, validated_data)
