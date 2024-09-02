import uuid
from django.db import models
from cloudinary.models import CloudinaryField
from authentication.models import CustomUser, UserBusiness
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from listing.choices import STATUS_TYPE


class Specifications(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    tag = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['-updated_on']


class CarType(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=250)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_on']


class CarModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=250)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_on']


class Amenities(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    tag = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    thumbnail = CloudinaryField('image', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['-updated_on']


class DiscountOption(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_on']


class ShortletListing(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    # Business Details
    business = models.ForeignKey(UserBusiness, on_delete=models.CASCADE)
    address = models.TextField()
    landmark_1 = models.TextField()
    landmark_2 = models.TextField()
    landmark_3 = models.TextField()
    # Listing Details
    product_name = models.CharField(max_length=250)
    product_description = models.TextField(null=True, blank=True)
    thumbnail_1 = CloudinaryField('image', null=True, blank=True)
    thumbnail_2 = CloudinaryField('image', null=True, blank=True)
    thumbnail_3 = CloudinaryField('image', null=True, blank=True)
    thumbnail_4 = CloudinaryField('image', null=True, blank=True)
    thumbnail_5 = CloudinaryField('image', null=True, blank=True)
    thumbnail_6 = CloudinaryField('image', null=True, blank=True)
    specification = models.ManyToManyField(Specifications)
    amenities = models.ManyToManyField(Amenities)
    type_of_apartment = models.CharField(max_length=250)
    utility_service_staffs = models.CharField(max_length=250)
    max_guests = models.IntegerField()
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    discount = models.CharField(max_length=250)
    discount_option = models.ForeignKey(
        DiscountOption, on_delete=models.CASCADE)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    proof_of_ownership = CloudinaryField('image', null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_TYPE, default='PENDING')
    is_approved = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-updated_on']


class CarListing(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    # Business Details
    business = models.ForeignKey(UserBusiness, on_delete=models.CASCADE)
    address = models.TextField()
    landmark_1 = models.TextField()
    landmark_2 = models.TextField()
    landmark_3 = models.TextField()
    # Listing Details
    product_name = models.CharField(max_length=250)
    product_description = models.TextField(null=True, blank=True)
    thumbnail_1 = CloudinaryField('image', null=True, blank=True)
    thumbnail_2 = CloudinaryField('image', null=True, blank=True)
    thumbnail_3 = CloudinaryField('image', null=True, blank=True)
    thumbnail_4 = CloudinaryField('image', null=True, blank=True)
    thumbnail_5 = CloudinaryField('image', null=True, blank=True)
    thumbnail_6 = CloudinaryField('image', null=True, blank=True)

    specification = models.ManyToManyField(Specifications)
    amenities = models.ManyToManyField(Amenities)

    type_of_car = models.OneToOneField(
        CarType, on_delete=models.SET_NULL, null=True, blank=True)
    car_model = models.OneToOneField(
        CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_driver = models.BooleanField(default=False)

    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    discount = models.CharField(max_length=250)
    discount_option = models.ForeignKey(
        DiscountOption, on_delete=models.CASCADE)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    proof_of_ownership = CloudinaryField('image', null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_TYPE, default='PENDING')
    is_approved = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-updated_on']


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    listing = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
