from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'full_name',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
    )
    list_filter = (
        'full_name',
        'email',
        'is_staff',
        'is_active',
        'is_superuser',
    )
    search_fields = (
        'full_name',
        'email',
    )
    ordering = (
        'email',
    )

    fieldsets = (
        (
            'User Info & Authentication',
            {
                'fields': (
                    'email',
                    'full_name',
                    'password',
                )
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                ),
            },
        ),
        (
            'Group Permissions',
            {
                'fields': (
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Important Dates',
            {
                'fields': (
                    'last_login',
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'full_name',
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                ),
            }
        ),
    )

admin.site.register(User, UserAdmin)