from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'name', )
    ordering = ('-name',)
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username',
                           'email',
                           'name',
                           'password',
                           'avatar',
                           'bio',
                           'is_superuser', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff'),
        },
        ),
    )


admin.site.register(User, UserAdminConfig)
