import uuid
import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField


def get_image_upload_path(instance, filename):
    folder_path = f"titanium_training/user/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(
        max_length=50, null=True, blank=True)
    last_name = models.CharField(
        max_length=50, null=True, blank=True)
    image = CloudinaryField('image', transformation={
        'width': 500, 'height': 500, 'crop': 'fit'}, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, null=True, blank=True)
    registration_method = models.CharField(
        default="Email_password", max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_social_user = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'image',  'is_verified', 'is_social_user', 'is_business', ]

    def __str__(self):
        return str(self.email)

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_full_name(self):
        """
        Returns the full name for the user.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class BusinessCategory(models.Model):
    text = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class UserBusiness(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=250)
    category_type = models.ManyToManyField(BusinessCategory)
    business_country = models.CharField(max_length=250)
    business_state = models.CharField(max_length=250)
    business_postal_code = models.CharField(max_length=250)
    business_city = models.SlugField(null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name
