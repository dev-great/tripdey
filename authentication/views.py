# views.py
import os
import logging
import base64
import random
from urllib.parse import urlencode
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404, redirect
from authentication.models import BusinessCategory, CustomUser, UserBusiness
from exceptions.custom_apiexception_class import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from dotenv import load_dotenv
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from utils.custom_response import custom_response
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .serializers import BusinessCategorySerializer, ChangePasswordSerializer, UserBusinessSerializer, UserSerializer, TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer, TokenVerifyResponseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

load_dotenv()
User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            logger.info(f"User registered: {serializer.data['email']}")
            return custom_response(status_code=status.HTTP_201_CREATED, message="Success", data=response_data)
        else:
            error_msg = str(serializer.errors)
            logger.error(f"Registration error: {error_msg}")
            return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class LoginView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Login request received.")
        print(request.data)
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            logger.info("Request data is valid.")
        except TokenError as e:
            logger.error(f"TokenError encountered: {e}")
            return CustomAPIException(
                detail="Invalid token.", status_code=status.HTTP_401_UNAUTHORIZED).get_full_details()
        except Exception as e:
            logger.error(f"Exception encountered: {e}")
            return CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

        logger.info("Login successful.")

        user_email = request.data['email']
        print(user_email)
        try:
            profile = CustomUser.objects.get(email__iexact=user_email)
        except CustomUser.DoesNotExist:
            logger.error(f"User with email {user_email} does not exist.")
            return CustomAPIException(
                detail="User not found.",
                status_code=status.HTTP_404_NOT_FOUND
            ).get_full_details()

        user_data = UserSerializer(profile).data

        # Include user details and tokens in the response
        response_data = {
            "auth": {
                "refresh": serializer.validated_data['refresh'],
                "access": serializer.validated_data['access'],
            },
            "user": user_data,
        }

        return custom_response(status_code=status.HTTP_200_OK, message="Success", data=response_data)


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Token refresh request received.")
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Token refresh successful.")
            return custom_response(status_code=status.HTTP_200_OK, message="Token is refresh.", data=response.data)
        else:
            logger.error(
                f"Token refresh failed with status code {response.status_code}.")
            return CustomAPIException(detail="Token is invalid.", status_code=response.status_code, data=response.data).get_full_details()


class TokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Token verification request received.")
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Token verification successful.")
            return custom_response(status_code=status.HTTP_200_OK, message="Token is valid.", data=response.data)
        else:
            logger.error(
                f"Token verification failed with status code {response.status_code}.")
            return CustomAPIException(detail="Token is invalid or expired.", status_code=response.status_code, data=response.data).get_full_details()


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request):
        logger.info(
            f"UserProfile PATCH request received for user: {request.user.email}")
        user_email = request.user.email

        try:
            profile = CustomUser.objects.get(email__exact=user_email)
            logger.debug(f"User profile found for email: {user_email}")
        except CustomUser.DoesNotExist:
            logger.error(f"User profile not found for email: {user_email}")
            raise CustomAPIException(
                detail="User profile not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        serializers = UserSerializer(profile, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            logger.info(
                f"User profile updated successfully for email: {user_email}")
            return custom_response(status_code=status.HTTP_200_OK, message="User updated successfully", data=serializers.data)

        logger.error(
            f"User profile update failed for email: {user_email}, errors: {serializers.errors}")
        raise CustomAPIException(
            detail=serializers.errors, status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

    def get(self, request):
        logger.info(
            f"UserProfile GET request received for user: {request.user.email}")
        email = request.user.email

        try:
            profile = CustomUser.objects.get(email__exact=email)
            logger.debug(f"User profile found for email: {email}")
        except CustomUser.DoesNotExist:
            logger.error(f"User profile not found for email: {email}")
            raise CustomAPIException(
                detail="User profile not found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

        serializer = UserSerializer(profile)
        logger.info(f"User profile retrieved successfully for email: {email}")
        return custom_response(status_code=status.HTTP_200_OK, message="Success.", data=serializer.data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'refresh', openapi.IN_QUERY, description="Refresh token", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            status.HTTP_205_RESET_CONTENT: "Logout successful.",
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request):
        logger.info(
            f"Logout POST request received for user: {request.user.email}")

        try:
            refresh_token = request.data['refresh']
            logger.debug(f"Refresh token received: {refresh_token}")

            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(
                f"Token blacklisted successfully for user: {request.user.email}")
            return custom_response(status_code=status.HTTP_205_RESET_CONTENT, message="Logout successful.", data=None)

        except Exception as e:
            logger.error(
                f"Logout failed for user: {request.user.email}, error: {str(e)}")
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        logger.info(
            f"ChangePassword update request received for user: {request.user.email}")

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                logger.warning(
                    f"Invalid old password provided by user: {request.user.email}")
                return CustomAPIException(
                    detail="Invalid Credential",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data={"old_password": ["Wrong password."]}
                ).get_full_details()

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            logger.info(
                f"Password updated successfully for user: {request.user.email}")

            return custom_response(status_code=status.HTTP_200_OK, message='Password updated successfully', data=None)

        logger.error(
            f"Password update failed for user: {request.user.email}, errors: {serializer.errors}")
        return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_email = self.request.user.email
        logger.info(f"Fetching user object for email: {user_email}")
        return get_object_or_404(CustomUser, email=user_email)

    def delete(self, request, *args, **kwargs):
        try:
            user_email = request.user.email
            logger.info(f"Delete request received for user: {user_email}")

            paysita_user = self.get_object()
            self.perform_destroy(paysita_user)
            logger.info(f"User deleted successfully: {user_email}")

            return custom_response(status_code=status.HTTP_200_OK, message="User deleted", data=None)
        except CustomUser.DoesNotExist:
            logger.warning(f"User not found for email: {user_email}")
            return CustomAPIException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            logger.error(f"Error deleting user {user_email}: {str(e)}")
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

    def perform_destroy(self, instance):
        instance.delete()
        logger.info(f"User instance deleted: {instance.email}")


otp_storage = {}


class EmailOTPAuthentication(APIView):
    def post(self, request):
        email = request.data.get('email')

        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Store the OTP with the email as the key
        otp_storage[email] = otp

        merge_data = {
            'inshopper_user': request.user.email,
            'otp': otp,
        }
        html_body = render_to_string(
            "emails/otp_mail.html", merge_data)
        msg = EmailMultiAlternatives(
            subject="Email Verification OTP.",
            from_email=os.getenv('EMAIL_USER'),
            to=[request.user.email],
            body=" ",
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return custom_response(status_code=status.HTTP_200_OK, message="OTP sent to your email.", data=None)

    def put(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        if email not in otp_storage:
            return CustomAPIException(detail="OTP not sent for this email.", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()

        if otp_entered == otp_storage[email]:
            del otp_storage[email]
            return custom_response(status_code=status.HTTP_200_OK, message="Email verification successful.", data=None)
        else:
            return CustomAPIException(detail="Incorrect OTP.", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class BusinesscategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            amenity = BusinessCategory.objects.all()
        except BusinessCategory.DoesNotExist:
            error_msg = f"Business category not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Business category: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = BusinessCategorySerializer(amenity, many=True)
        return custom_response(status_code=status.HTTP_200_OK, message="Business category fetched successfully", data=serializer.data)

    @swagger_auto_schema(
        request_body=BusinessCategorySerializer(many=True),
        responses={
            status.HTTP_201_CREATED: BusinessCategorySerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = BusinessCategorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Business category created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

    @swagger_auto_schema(request_body=BusinessCategorySerializer)
    def put(self, request, pk, format=None):
        try:
            business_category = BusinessCategory.objects.get(id=pk)
        except BusinessCategory.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Business category not found or you do not have permission to edit this Business category")
        try:
            serializer = BusinessCategorySerializer(
                business_category, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Business category updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            business_category = BusinessCategory.objects.get(id=pk)
            business_category.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Business category deleted successfully")

        except business_category.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Business category not found or you do not have permission to delete this Business category")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class UserBusinessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_businesses = UserBusiness.objects.filter(
                user=request.user).prefetch_related('category_type')
        except UserBusiness.DoesNotExist:
            error_msg = f"User business not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the User business: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = UserBusinessSerializer(user_businesses, many=True)
        return custom_response(status_code=status.HTTP_200_OK, message="User business fetched successfully", data=serializer.data)

    @swagger_auto_schema(
        request_body=UserBusinessSerializer(many=True),
        responses={status.HTTP_201_CREATED: UserBusinessSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserBusinessSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="User business created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

    @swagger_auto_schema(request_body=UserBusinessSerializer)
    def put(self, request, pk, format=None):
        try:
            user_business = UserBusiness.objects.get(id=pk)
        except UserBusiness.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="User business not found or you do not have permission to edit this User business")
        try:
            serializer = UserBusinessSerializer(
                user_business, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="User business updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            amenity = UserBusiness.objects.get(id=pk, user=request.user)
            amenity.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="User business deleted successfully")

        except amenity.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="User business not found or you do not have permission to delete this User business")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class GoogleAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImIyZjgwYzYzNDYwMGVkMTMwNzIxMDFhOGI0MjIwNDQzNDMzZGIyODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzNTA1NTU0NTA2OTMtOWJhYTE3MjdxYzI4aTdpOGcwc3NoaDRhNTJhYTMzMW8uYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzNTA1NTU0NTA2OTMtZ2ppYnFhcXRxdDZxMW8wNjF2YXBzNDZjMGNzN3BvY2kuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTM1ODc2MTQxMzU4Mjg2NDcyNzAiLCJlbWFpbCI6ImdtYXJzaGFsMDcwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiR3JlYXRuZXNzIE1hcnNoYWwiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSVl6dnZLbXFHcWRfYzFwTG5qZG9vQXBrSU12ZGJUNTAwWTg4ZE9GSnBZdEQycDBJOXo9czk2LWMiLCJnaXZlbl9uYW1lIjoiR3JlYXRuZXNzIiwiZmFtaWx5X25hbWUiOiJNYXJzaGFsIiwiaWF0IjoxNzI1NDQ5Nzk1LCJleHAiOjE3MjU0NTMzOTV9.of5fqF5lC_I_3PnOh_G17a66SASvpOq6xkrrJj1Y0TyptTaWNHJB92Aoy7aOK17DO1gHS8gAQoLHMrSBusj0_5lKkdTx6nocDpSYkjCdjz6qUhQeE8Z8J_vP4pNGMM8kShfgijuFTeP1jn_vscF0E9hYRgRH2tKAh6KIpoKM0625b_GFdsj1pBg1MrpmQLC_k21ZUMLjY1yU70RKc4frwE9G1NvWc7YCO0CQ"
        CLIENT_ID = "350555450693-gjibqaqtqt6q1o061vaps46c0cs7poci.apps.googleusercontent.com"
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), "350555450693-gjibqaqtqt6q1o061vaps46c0cs7poci.apps.googleusercontent.com")

            print("Token is valid:", idinfo)
            return custom_response(status_code=status.HTTP_200_OK, message="User success", data=idinfo)

        except Exception as e:
            return CustomAPIException(
                detail=str(e), status_code=status.HTTP_404_NOT_FOUND).get_full_details()
