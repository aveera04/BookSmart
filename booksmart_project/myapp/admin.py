from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import User, Genre, Book
from django.utils.html import format_html

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

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def book_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="100" />',obj.image.url)
        return ""
    list_display = ('title','isbn', 'author','description','price', 'genre', 'publisher', 'published_date','book_image')


