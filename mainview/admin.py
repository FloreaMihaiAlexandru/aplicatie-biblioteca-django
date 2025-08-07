from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .models import Book, Rent
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'available_copies')
    search_fields = ('title', 'author')
    list_filter = ('published_date', 'available_copies')
    ordering = ('title', '-published_date')
    list_per_page = 20

@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rent_date', 'return_date')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rent_date', 'return_date')
    ordering = ('-rent_date',)
    list_per_page = 20

@admin.action(description="Verify user")
def make_users_active(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


class CustomUserAdmin(UserAdmin):
    actions = [make_users_active, deactivate_users]

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
