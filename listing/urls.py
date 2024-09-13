from django.urls import path
from .views import (
    CarModelAPIView,
    CarModelCreateAPIView,
    CarModelCreateAPIView,
    AmenitiesCreateAPIView,
    SpecificationsCreateAPIView,
    DiscountOptionCreateAPIView,
    CarListingCreateAPIView,
    ReviewCreateAPIView,
    ShortletListingCreateAPIView,
    CarModelAPIView,
    AmenitiesAPIView,
    SpecificationsAPIView,
    DiscountOptionAPIView,
    CarListingAPIView,
    ReviewAPIView,
    ShortletListingAPIView,
    GetAllShortletListAPIView,
    GetAllCarRentalListAPIView

)
app_name = 'listing'
urlpatterns = [
    # CarType URLs
    path('car-types/<int:pk>/', CarModelAPIView.as_view(), name='car-type-detail'),
    path('car-types/', CarModelCreateAPIView.as_view(), name='car-type-list'),

    # CarModel URLs
    path('car-models/<int:pk>/', CarModelAPIView.as_view(), name='car-model-detail'),
    path('car-models/', CarModelCreateAPIView.as_view(), name='car-model-list'),

    # Amenities URLs
    path('amenities/<int:pk>/', AmenitiesAPIView.as_view(), name='amenity-detail'),
    path('amenities/', AmenitiesCreateAPIView.as_view(), name='amenity-list'),

    # Specifications URLs
    path('specifications/<int:pk>/', SpecificationsAPIView.as_view(),
         name='specification-detail'),
    path('specifications/', SpecificationsCreateAPIView.as_view(),
         name='specification-list'),

    # DiscountOption URLs
    path('discount-options/<int:pk>/', DiscountOptionAPIView.as_view(),
         name='discount-option-detail'),
    path('discount-options/', DiscountOptionCreateAPIView.as_view(),
         name='discount-option-list'),

    # CarListing URLs
    path('car-listings/<int:pk>/', CarListingAPIView.as_view(),
         name='car-listing-detail'),
    path('car-listings/', CarListingCreateAPIView.as_view(),
         name='car-listing-list'),

    # Review API
    path('reviews/<uuid:pk>/', ReviewAPIView.as_view(), name='review-detail'),
    path('reviews/', ReviewCreateAPIView.as_view(), name='review-list'),

    # Shortlet Listing API
    path('shortlet-listings/<uuid:pk>/', ShortletListingAPIView.as_view(),
         name='shortlet-listing-detail'),
    path('shortlet-listings/', ShortletListingCreateAPIView.as_view(),
         name='shortlet-listing-list'),

    # Get All Shortlet Listings API
    path('shortlet-listings/all/', GetAllShortletListAPIView.as_view(),
         name='all-shortlet-listings'),

    # Get All Car Rentals API
    path('car-rentals/all/', GetAllCarRentalListAPIView.as_view(),
         name='all-car-rentals'),
]
