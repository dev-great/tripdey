from django.shortcuts import render

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from authentication.models import UserBusiness
from listing.models import Amenities, CarListing, CarModel, CarType, DiscountOption, Review, ShortletListing, Specifications
from listing.serializers import AmenitiesSerializer, CarListingSerializer, CarModelSerializer, CarTypeSerializer, DiscountOptionSerializer, ReviewSerializer, ShortletListingSerializer, SpecificationsSerializer
from utils.custom_response import custom_response
from rest_framework.permissions import AllowAny, IsAuthenticated
from exceptions.custom_apiexception_class import CustomAPIException
# Create your views here.


class CarModelCreateAPIView(APIView):

    @swagger_auto_schema(
        request_body=CarTypeSerializer(many=True),
        responses={status.HTTP_201_CREATED: CarTypeSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = CarTypeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Car type created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()


class CarModelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            car_model = CarType.objects.get(id=pk)
        except CarType.DoesNotExist:
            error_msg = f"Car type with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Car model: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = CarTypeSerializer(car_model)
        return custom_response(status_code=status.HTTP_200_OK, message="Car type fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=CarTypeSerializer)
    def put(self, request, pk, format=None):
        try:
            car_type = CarType.objects.get(id=pk)
        except CarType.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car type not found or you do not have permission to edit this Car type")
        try:
            serializer = CarTypeSerializer(
                car_type, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Car type updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            car_type = CarType.objects.get(id=pk)
            car_type.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Car type deleted successfully")

        except CarModel.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car type not found or you do not have permission to delete this Car type")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class CarModelCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=CarModelSerializer(many=True),
        responses={status.HTTP_201_CREATED: CarModelSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = CarModelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Car model created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()


class CarModelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            car_model = CarModel.objects.get(id=pk)
        except CarModel.DoesNotExist:
            error_msg = f"Car model with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Car model: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = CarModelSerializer(car_model)
        return custom_response(status_code=status.HTTP_200_OK, message="Car model fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=CarModelSerializer)
    def put(self, request, pk, format=None):
        try:
            car_model = CarModel.objects.get(id=pk)
        except CarModel.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car model not found or you do not have permission to edit this Car model")
        try:
            serializer = CarModelSerializer(
                car_model, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Car model updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            car_model = CarModel.objects.get(id=pk)
            car_model.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Car model deleted successfully")

        except CarModel.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car model not found or you do not have permission to delete this Car model")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class AmenitiesCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=AmenitiesSerializer(many=True),
        responses={status.HTTP_201_CREATED: AmenitiesSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = AmenitiesSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Amenity created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()


class AmenitiesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            amenity = Amenities.objects.get(id=pk)
        except Amenities.DoesNotExist:
            error_msg = f"Amenity with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Amenity: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = AmenitiesSerializer(amenity)
        return custom_response(status_code=status.HTTP_200_OK, message="Amenities fetched successfully", data=serializer.data)

    @swagger_auto_schema(
        request_body=AmenitiesSerializer(many=True),
        responses={status.HTTP_201_CREATED: AmenitiesSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = AmenitiesSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Amenity created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()

    @swagger_auto_schema(request_body=AmenitiesSerializer)
    def put(self, request, pk, format=None):
        try:
            amenity = Amenities.objects.get(id=pk)
        except amenity.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Amenity not found or you do not have permission to edit this Amenity")
        try:
            serializer = AmenitiesSerializer(
                amenity, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Amenity updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            amenity = Amenities.objects.get(id=pk)
            amenity.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Amenity deleted successfully")

        except amenity.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Amenity not found or you do not have permission to delete this Amenity")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class SpecificationsCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=SpecificationsSerializer(many=True),
        responses={
            status.HTTP_201_CREATED: SpecificationsSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = SpecificationsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Specification created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()


class SpecificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            specification = Specifications.objects.get(id=pk)
        except Specifications.DoesNotExist:
            error_msg = f"Specification with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Specification: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = SpecificationsSerializer(specification)
        return custom_response(status_code=status.HTTP_200_OK, message="Specification fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=SpecificationsSerializer)
    def put(self, request, pk, format=None):
        try:
            specification = Specifications.objects.get(id=pk)
        except specification.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Specification not found or you do not have permission to edit this Specification")
        try:
            serializer = SpecificationsSerializer(
                specification, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Specification updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            specification = Specifications.objects.get(id=pk)
            specification.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Specification deleted successfully")

        except specification.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Specification not found or you do not have permission to delete this Specification")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class DiscountOptionCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=DiscountOptionSerializer(many=True),
        responses={
            status.HTTP_201_CREATED: DiscountOptionSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        serializer = DiscountOptionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                response_data = serializer.data
                return custom_response(status_code=status.HTTP_201_CREATED, message="Discount option created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(
                    e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(
                detail="Invalid data found.", status_code=status.HTTP_404_NOT_FOUND).get_full_details()


class DiscountOptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            discountOption = DiscountOption.objects.get(id=pk)
        except DiscountOption.DoesNotExist:
            error_msg = f"Discount option with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Discount option: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = SpecificationsSerializer(discountOption)
        return custom_response(status_code=status.HTTP_200_OK, message="Discount option fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=DiscountOptionSerializer)
    def put(self, request, pk, format=None):
        try:
            discountOption = DiscountOption.objects.get(id=pk)
        except discountOption.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Discount option not found or you do not have permission to edit this Discount option")
        try:
            serializer = SpecificationsSerializer(
                discountOption, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Discount option updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            discountOption = DiscountOption.objects.get(id=pk)
            discountOption.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Discount option deleted successfully")

        except discountOption.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Discount option not found or you do not have permission to delete this Discount option")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class CarListingCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amenities': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    example=["uuid-of-amenity-1", "uuid-of-amenity-2"]
                ),
                'specification': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    example=["uuid-of-specification-1",
                             "uuid-of-specification-2"]
                ),
                'type_of_car': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="uuid-of-car-type"
                ),
                'car_model': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="uuid-of-car-model"
                ),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        try:
            business = UserBusiness.objects.get(user=user)
        except UserBusiness.DoesNotExist:
            return custom_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User business not found."
            )

        def get_or_create_amenities(tags):
            amenities = []
            for tag in tags:
                obj, created = Amenities.objects.get_or_create(tag=tag)
                amenities.append(obj)
            return amenities

        def get_or_create_specifications(tags):
            specifications = []
            for tag in tags:
                obj, created = Specifications.objects.get_or_create(tag=tag)
                specifications.append(obj)
            return specifications

        def get_or_create_car_type(title):
            obj, created = CarType.objects.get_or_create(title=title)
            return obj

        def get_or_create_car_model(title):
            obj, created = CarModel.objects.get_or_create(title=title)
            return obj

        # Process each item in the request data
        processed_data = []
        for item in data:
            item['user'] = user.id
            item['business'] = business.id

            # Get or create amenities
            if 'amenities' in item:
                item['amenities'] = [
                    amenity.id for amenity in get_or_create_amenities(item['amenities'])]

            # Get or create specifications
            if 'specification' in item:
                item['specification'] = [
                    spec.id for spec in get_or_create_specifications(item['specification'])]

            # Get or create car type and car model
            if 'type_of_car' in item:
                item['type_of_car'] = get_or_create_car_type(
                    item['type_of_car']).id
            if 'car_model' in item:
                item['car_model'] = get_or_create_car_model(
                    item['car_model']).id

            processed_data.append(item)

        # Serialize and validate the data
        serializer = CarListingSerializer(data=processed_data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return custom_response(
                    status_code=status.HTTP_201_CREATED,
                    message="Car listing created successfully",
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


class CarListingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            amenity = CarListing.objects.get(id=pk)
        except CarListing.DoesNotExist:
            error_msg = f"Car listing with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the car listing: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = CarListingSerializer(amenity)
        return custom_response(status_code=status.HTTP_200_OK, message="Car Listing fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=CarListingSerializer)
    def put(self, request, pk, format=None):
        try:
            carListing = CarListing.objects.get(id=pk)
        except CarListing.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car Listing not found or you do not have permission to edit this Car Listing")
        try:
            serializer = CarListingSerializer(
                carListing, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Car Listing updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            carListing = CarListing.objects.get(
                id=pk, user=request.user)
            carListing.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Car Listing deleted successfully")

        except carListing.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Car Listing not found or you do not have permission to delete this Car Listing")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class ReviewCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='UUID of the user'),
                'content_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of listing (ShortletListing or CarListing)'),
                'object_id': openapi.Schema(type=openapi.TYPE_STRING, description='UUID of the listing'),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating (1 to 5)'),
                'review': openapi.Schema(type=openapi.TYPE_STRING, description='Review text'),
            }
        ),
        responses={
            status.HTTP_201_CREATED: ReviewSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid data found.",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Check if the content type and object ID are valid
                content_type = serializer.validated_data['content_type']
                object_id = serializer.validated_data['object_id']
                model = ContentType.objects.get(
                    model=content_type).model_class()

                # Check if the object exists
                if not model.objects.filter(id=object_id).exists():
                    raise CustomAPIException(
                        detail="Invalid listing specified.", status_code=status.HTTP_404_NOT_FOUND)

                serializer.save()
                return custom_response(status_code=status.HTTP_201_CREATED, message="Review created successfully", data=serializer.data)
            except Exception as e:
                return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
        else:
            return CustomAPIException(detail="Invalid data found.", status_code=status.HTTP_400_BAD_REQUEST).get_full_details()


class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            review = Review.objects.get(id=pk)
        except Review.DoesNotExist:
            error_msg = f"Review with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the Review: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = ReviewSerializer(review)
        return custom_response(status_code=status.HTTP_200_OK, message="Review fetched successfully", data=serializer.data)


class ShortletListingCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amenities': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    example=["uuid-of-amenity-1", "uuid-of-amenity-2"]
                ),
                'specification': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    example=["uuid-of-specification-1",
                             "uuid-of-specification-2"]
                ),
                'type_of_apartment': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="uuid-of-apartment-type"
                ),
                'utility_service_staffs': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="uuid-of-utility-service-staffs"
                ),
                'discount_option': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="uuid-of-discount-option"
                ),
                'price_per_day': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    example=100.00
                ),
                'discount_price': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    example=80.00
                ),
                # Other fields as necessary
            }
        )
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        try:
            business = UserBusiness.objects.get(user=user)
        except UserBusiness.DoesNotExist:
            return custom_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User business not found."
            )

        def get_or_create_amenities(tags):
            amenities = []
            for tag in tags:
                obj, created = Amenities.objects.get_or_create(tag=tag)
                amenities.append(obj)
            return amenities

        def get_or_create_specifications(tags):
            specifications = []
            for tag in tags:
                obj, created = Specifications.objects.get_or_create(tag=tag)
                specifications.append(obj)
            return specifications

        def get_or_create_discount_option(title):
            obj, created = DiscountOption.objects.get_or_create(title=title)
            return obj

        # Process each item in the request data
        processed_data = []
        for item in data:
            item['user'] = user.id
            item['business'] = business.id

            # Get or create amenities
            if 'amenities' in item:
                item['amenities'] = [
                    amenity.id for amenity in get_or_create_amenities(item['amenities'])]

            # Get or create specifications
            if 'specification' in item:
                item['specification'] = [
                    spec.id for spec in get_or_create_specifications(item['specification'])]

            # Get or create discount option
            if 'discount_option' in item:
                item['discount_option'] = get_or_create_discount_option(
                    item['discount_option']).id

            processed_data.append(item)

        # Serialize and validate the data
        serializer = ShortletListingSerializer(data=processed_data, many=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return custom_response(
                    status_code=status.HTTP_201_CREATED,
                    message="Shortlet listing created successfully",
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


class ShortletListingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            shortlet_listing = ShortletListing.objects.get(id=pk)
        except ShortletListing.DoesNotExist:
            error_msg = f"Shortlet listing with id {pk} not found."
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_404_NOT_FOUND).get_full_details()
        except Exception as e:
            error_msg = f"An error occurred while retrieving the shortlet listing: {str(e)}"
            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

        serializer = ShortletListingSerializer(shortlet_listing)
        return custom_response(status_code=status.HTTP_200_OK, message="Shortlet listing fetched successfully", data=serializer.data)

    @swagger_auto_schema(request_body=ShortletListingSerializer)
    def put(self, request, pk, format=None):
        try:
            shortlet_listing = ShortletListing.objects.get(id=pk)
        except ShortletListing.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Shortlet listing not found or you do not have permission to edit this Shortlet listing")
        try:
            serializer = ShortletListingSerializer(
                shortlet_listing, data=request.data, partial=False)

            if serializer.is_valid():
                serializer.save()
                return custom_response(status_code=status.HTTP_200_OK, message="Shortlet listing updated successfully", data=serializer.data)
            else:
                return custom_response(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))

    @swagger_auto_schema(responses={204: "Success", 404: "Not found"})
    def delete(self, request, pk, format=None):
        try:
            shortlet_listing = ShortletListing.objects.get(
                id=pk, user=request.user)
            shortlet_listing.delete()
            return custom_response(status_code=status.HTTP_204_NO_CONTENT, message="Shortlet listing deleted successfully")

        except ShortletListing.DoesNotExist:
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, message="Shortlet listing not found or you do not have permission to delete this Shortlet listing")
        except Exception as e:
            return custom_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An unexpected error occurred", data=str(e))


class GetAllShortletListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # Fetch query parameters
            product_name = request.query_params.get('product_name', None)
            address = request.query_params.get('address', None)
            status = request.query_params.get('status', None)
            is_approved = request.query_params.get('is_approved', None)
            is_booked = request.query_params.get('is_booked', None)
            amenities = request.query_params.getlist(
                'amenities', None)  # Expecting a list of amenities
            type_of_apartment = request.query_params.get(
                'type_of_apartment', None)

            # Base filter for fetching shortlets owned by the user
            filters = Q(user=request.user)

            # Apply filters based on query parameters
            if product_name:
                filters &= Q(product_name__icontains=product_name)
            if address:
                filters &= Q(address__icontains=address)
            if status:
                filters &= Q(status__iexact=status)
            if is_approved is not None:
                filters &= Q(is_approved=bool(int(is_approved)))
            if is_booked is not None:
                filters &= Q(is_booked=bool(int(is_booked)))
            if type_of_apartment:
                filters &= Q(type_of_apartment__iexact=type_of_apartment)
            if amenities:
                filters &= Q(amenities__name__in=amenities)

            # Fetch filtered shortlet listings
            shortlets = ShortletListing.objects.filter(
                filters).distinct().order_by('-updated_on')
            if not shortlets.exists():
                return CustomAPIException(
                    detail="No shortlets found for this user",
                    status_code=status.HTTP_404_NOT_FOUND
                ).get_full_details()

            shortlets_data = []

            # Retrieve and serialize shortlets and their reviews
            for shortlet in shortlets:
                try:
                    # Get content type for ShortletListing
                    content_type = ContentType.objects.get_for_model(
                        ShortletListing)

                    # Retrieve reviews related to the shortlet using GenericForeignKey
                    reviews = Review.objects.filter(
                        content_type=content_type, object_id=shortlet.id)
                    shortlet_data = ShortletListingSerializer(shortlet).data
                    reviews_data = []

                    for review in reviews:
                        review_data = {
                            'user': review.user.id,
                            'rating': review.rating,
                            'review': review.review,
                            'created_on': review.created_on
                        }
                        reviews_data.append(review_data)

                    # Add reviews to the shortlet data
                    shortlet_data['reviews'] = reviews_data
                    shortlets_data.append(shortlet_data)
                except Exception as e:
                    error_msg = f"An error occurred while retrieving the reviews for shortlet {shortlet.id}: {str(e)}"

                    return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

            # Prepare the final response
            response_data = {
                "shortlets": shortlets_data
            }

            return custom_response(status_code=status.HTTP_200_OK, message="Shortlets and reviews fetched successfully", data=response_data)

        except Exception as e:
            error_msg = f"An error occurred while retrieving the shortlets: {str(e)}"

            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()


class GetAllCarRentalListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # Fetch query parameters
            car_model = request.query_params.get('car_model', None)
            car_type = request.query_params.get('car_type', None)
            rental_status = request.query_params.get('rental_status', None)
            is_approved = request.query_params.get('is_approved', None)
            is_booked = request.query_params.get('is_booked', None)
            amenities = request.query_params.getlist(
                'amenities', None)  # Expecting a list of amenities
            type_of_car = request.query_params.get('type_of_car', None)

            # Base filter for fetching car rentals owned by the user
            filters = Q(user=request.user)

            # Apply filters based on query parameters
            if car_model:
                filters &= Q(car_model__icontains=car_model)
            if car_type:
                filters &= Q(car_type__icontains=car_type)
            if rental_status:
                filters &= Q(rental_status__iexact=rental_status)
            if is_approved is not None:
                filters &= Q(is_approved=bool(int(is_approved)))
            if is_booked is not None:
                filters &= Q(is_booked=bool(int(is_booked)))
            if type_of_car:
                filters &= Q(type_of_car__iexact=type_of_car)
            if amenities:
                filters &= Q(amenities__name__in=amenities)

            # Fetch filtered car rentals
            car_rentals = CarListing.objects.filter(
                filters).distinct().order_by('-updated_on')
            if not car_rentals.exists():
                return CustomAPIException(
                    detail="No car rentals found for this user",
                    status_code=status.HTTP_404_NOT_FOUND
                ).get_full_details()

            car_rentals_data = []

            for car_rental in car_rentals:
                try:
                    content_type = ContentType.objects.get_for_model(
                        CarListing)

                    reviews = Review.objects.filter(
                        content_type=content_type, object_id=car_rental.id)
                    car_rental_data = CarListingSerializer(car_rental).data
                    reviews_data = []

                    for review in reviews:
                        review_data = {
                            'user': review.user.id,
                            'rating': review.rating,
                            'review': review.review,
                            'created_on': review.created_on
                        }
                        reviews_data.append(review_data)

                    car_rental_data['reviews'] = reviews_data
                    car_rentals_data.append(car_rental_data)
                except Exception as e:
                    error_msg = f"An error occurred while retrieving the reviews for car rental {car_rental.id}: {str(e)}"

                    return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()

            response_data = {
                "car_rentals": car_rentals_data
            }

            return custom_response(status_code=status.HTTP_200_OK, message="Car rentals and reviews fetched successfully", data=response_data)

        except Exception as e:
            error_msg = f"An error occurred while retrieving the car rentals: {str(e)}"

            return CustomAPIException(detail=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).get_full_details()
