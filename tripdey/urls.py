from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static

from tripdey.settings import STATIC_ROOT, STATIC_URL

schema_view = get_schema_view(
    openapi.Info(
        title="Tripdey API Documentation",
        default_version='v1',
        description="...",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="developer@tripdey.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authorization/',
         include('authentication.urls')),
    path('api/v1/bookings/',
         include('booking.urls')),
    path('api/v1/listings/',
         include('listing.urls')),

]


urlpatterns += [
    path('api/v1/docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

admin.site.site_header = 'Tripdey Control Panel'
admin.site.index_title = 'Administrators Dashboard'
admin.site.site_title = 'Control Panel'
