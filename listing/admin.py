from django.contrib import admin
from listing.models import Amenities, CarListing, DiscountOption, ShortletListing, Specifications
# Register your models here.

admin.site.register(Specifications)
admin.site.register(Amenities)
admin.site.register(DiscountOption)
admin.site.register(ShortletListing)
admin.site.register(CarListing)
