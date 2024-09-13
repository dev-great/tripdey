from django.urls import path
from .views import BookingAPIView
app_name = 'booking'
urlpatterns = [
    path('bookings/<uuid:pk>/', BookingAPIView.as_view(), name='booking-detail'),
    path('bookings/', BookingAPIView.as_view(), name='booking-list'),
]
