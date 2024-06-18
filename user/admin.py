from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

from .models import UserDetails, Member, Society

User = get_user_model()

admin.site.register(UserDetails)

# @admin.register(UserDetails)
# class UserDetailsAdmin(admin.ModelAdmin):
#     list_display = ('flat_number', 'age')
#     # Add any other configurations you need

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('society', 'user', 'user_details', 'flat_number', 'member_name', 'phone_no', 'age')
    # Add any other configurations you need

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('id', 'society_name', 'type', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('society_name',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected societies as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected societies as inactive"

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'image_preview', 'is_staff', 'is_active', 'society_name', 'type')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'phone_number', 'society_name')
    ordering = ('email',)
    list_display_links = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'phone_number', 'image', 'address', 'society_name', 'type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    filter_horizontal = ()
    readonly_fields = ('last_login',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px;" />'.format(obj.image.url))
        return 'No Image'

    image_preview.short_description = 'Image'
