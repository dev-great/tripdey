from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .forms import *
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {
         'fields': ('phone_number', 'image', 'is_verified', 'is_social_user', 'is_business')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ['email', 'first_name', 'last_name', 'phone_number',
                    'get_short_name', 'is_verified', 'is_social_user', 'is_business', 'is_staff']
    search_fields = ('email', 'first_name', 'last_name', 'phone_number',
                     )
    ordering = ('email', )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(BusinessCategory)
class BusinessCategogyAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_on', 'updated_on')
    search_fields = ('text',)
    ordering = ('-created_on',)


@admin.register(UserBusiness)
class UserBusinessAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'business_name', 'business_country', 'business_state',
        'business_postal_code', 'business_city', 'is_owner', 'created_on', 'updated_on'
    )
    list_filter = ('business_country', 'is_owner')
    search_fields = ('business_name', 'business_country',
                     'business_state', 'business_city')
    ordering = ('-created_on',)
