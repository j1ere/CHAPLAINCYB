from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'full_name', 'is_student',
        'is_staff', 'is_superuser', 'date_joined'
    )

    list_filter = ('is_staff', 'is_superuser', 'is_student', 'is_active')

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'full_name',
                'is_student',
                'prayer_house',
                'year_group',
                'small_christian_community',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'email',
                'full_name',
                'is_student',
                'prayer_house',
                'year_group',
                'small_christian_community',
            )
        }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)
