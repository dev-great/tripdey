from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from authentication.models import CustomUser


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='bookings')
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='owned_bookings')

    # Booking Details
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)

    # Booking Type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Additional Booking Information
    pick_up_location = models.CharField(max_length=255, null=True, blank=True)
    drop_off_location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        default=0.00
    )
    status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), (
        'CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')], default='PENDING')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} from {self.start_time} to {self.end_time}"

    class Meta:
        ordering = ['-created_on']
