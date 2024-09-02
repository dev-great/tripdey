# serializers.py

from rest_framework import serializers
from .models import Amenities, CarListing, CarModel, CarType, DiscountOption, Review, ShortletListing, Specifications
from authentication.serializers import UserBusinessSerializer, UserSerializer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarType
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class DiscountOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountOption
        fields = '__all__'
        read_only_fields = ['created_on', 'updated_on']


class ShortletListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    business = UserBusinessSerializer(read_only=True)
    specification = SpecificationsSerializer(many=True, read_only=True)
    amenities = AmenitiesSerializer(many=True, read_only=True)
    discount_option = DiscountOptionSerializer(read_only=True)

    class Meta:
        model = ShortletListing
        fields = '__all__'
        read_only_fields = ['user', 'business', 'created_on', 'updated_on']


class CarListingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    business = UserBusinessSerializer(read_only=True)
    specification = SpecificationsSerializer(many=True, read_only=True)
    amenities = AmenitiesSerializer(many=True, read_only=True)
    discount_option = DiscountOptionSerializer(read_only=True)

    class Meta:
        model = CarListing
        fields = '__all__'
        read_only_fields = ['user', 'business', 'created_on', 'updated_on']


class ReviewSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    object_id = serializers.UUIDField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'content_type',
                  'object_id', 'rating', 'review', 'created_on']
        read_only_fields = ['id', 'created_on']

    def validate(self, data):
        content_type = data.get('content_type')
        object_id = data.get('object_id')

        if content_type.model not in ['shortletlisting', 'carlisting']:
            raise serializers.ValidationError(
                "Invalid content type. Must be 'shortletlisting' or 'carlisting'.")

        model_class = content_type.model_class()
        if not model_class.objects.filter(id=object_id).exists():
            raise serializers.ValidationError(
                "Invalid object ID. The specified listing does not exist.")

        return data

    def create(self, validated_data):
        content_type = validated_data.pop('content_type')
        object_id = validated_data.pop('object_id')
        model_class = content_type.model_class()

        listing = model_class.objects.get(id=object_id)

        review = Review.objects.create(
            user=validated_data['user'],
            content_type=content_type,
            object_id=object_id,
            rating=validated_data['rating'],
            review=validated_data['review']
        )
        return review
