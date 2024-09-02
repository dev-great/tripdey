from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from authentication.serializers import UserSerializer
from booking.models import Booking
from listing.models import CarListing, ShortletListing
from listing.serializers import CarListingSerializer, ShortletListingSerializer


class BookingSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'owner', 'start_time', 'end_time', 'location', 'content_object',
                  'pick_up_location', 'drop_off_location', 'notes', 'price', 'status', 'created_on', 'updated_on']

    def get_content_object(self, obj):
        content_type = obj.content_type.model_class()
        if isinstance(obj.car_rental, CarListing):
            return CarListingSerializer(obj.car_rental).data
        elif isinstance(obj.shortlet, ShortletListing):
            return ShortletListingSerializer(obj.shortlet).data
        return None
