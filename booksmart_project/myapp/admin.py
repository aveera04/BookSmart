from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=User

    list_display=('email', 'is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)
    readonly_fields = ('date_joined',)

    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)