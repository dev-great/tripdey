# views.py
from booking.models import Booking
from booking.serializer import BookingSerializer
from exceptions.custom_apiexception_class import *
from rest_framework import status
from rest_framework.views import APIView
from utils.custom_response import custom_response
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.contenttypes.models import ContentType


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return CustomAPIException(
                detail=f"Booking with id {pk} not found.",
                status_code=status.HTTP_404_NOT_FOUND
            ).get_full_details()
        except Exception as e:
            return CustomAPIException(
                detail=f"An error occurred while retrieving the booking: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).get_full_details()

        serializer = BookingSerializer(booking)
        return custom_response(
            status_code=status.HTTP_200_OK,
            message="Booking fetched successfully",
            data=serializer.data
        )

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={
            status.HTTP_201_CREATED: BookingSerializer
        }
    )
    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                content_type_model = request.data.get('content_type')
                content_type = ContentType.objects.get(
                    model=content_type_model)
                content_object_id = request.data.get('content_object_id')
                content_object = content_type.get_object_for_this_type(
                    id=content_object_id)

                booking = serializer.save(
                    content_type=content_type, content_object=content_object)

                response_data = serializer.data
                return custom_response(
                    status_code=status.HTTP_201_CREATED,
                    message="Booking created successfully",
                    data=response_data
                )
            except Exception as e:
                return CustomAPIException(
                    detail=str(e),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                ).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.",
                status_code=status.HTTP_400_BAD_REQUEST
            ).get_full_details()

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={
            status.HTTP_200_OK: BookingSerializer
        }
    )
    def put(self, request, pk, format=None):
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            return CustomAPIException(
                detail=f"Booking with id {pk} not found.",
                status_code=status.HTTP_404_NOT_FOUND
            ).get_full_details()
        except Exception as e:
            return CustomAPIException(
                detail=f"An error occurred while retrieving the booking: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).get_full_details()

        serializer = BookingSerializer(
            booking, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return custom_response(
                    status_code=status.HTTP_200_OK,
                    message="Booking updated successfully",
                    data=serializer.data
                )
            except Exception as e:
                return CustomAPIException(
                    detail=str(e),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                ).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.",
                status_code=status.HTTP_400_BAD_REQUEST
            ).get_full_details()

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "No content",
            status.HTTP_404_NOT_FOUND: "Not found"
        }
    )
    def delete(self, request, pk, format=None):
        try:
            booking = Booking.objects.get(id=pk, user=request.user)
            booking.delete()
            return custom_response(
                status_code=status.HTTP_204_NO_CONTENT,
                message="Booking deleted successfully"
            )
        except Booking.DoesNotExist:
            return CustomAPIException(
                detail=f"Booking with id {pk} not found.",
                status_code=status.HTTP_404_NOT_FOUND
            ).get_full_details()
        except Exception as e:
            return CustomAPIException(
                detail=f"An error occurred while deleting the booking: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).get_full_details()
