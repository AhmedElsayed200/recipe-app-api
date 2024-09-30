""" django admin customization """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """ customize admin user """
    # Fields to display in the list view in the admin
    list_display = ['email', 'name']
    # Fields to filter in the right sidebar
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    # Fields to be used in the form for adding and updating users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),  # Removed first_name, last_name
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),  # Removed date_joined
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1','password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('id',)
    # Define read-only fields
    readonly_fields = ('last_login',)

admin.site.register(models.User, UserAdmin)