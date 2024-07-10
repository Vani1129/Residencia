from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

from .models import UserDetails, Member, Society, Type,FamilyMember,CustomUser

User = get_user_model()

admin.site.register(UserDetails)



@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
   

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'image_preview', 'is_staff', 'is_active', 'fullname', 'type')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'phone_number', 'name')
    ordering = ('email',)
    list_display_links = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'fullname', 'phone_number', 'image', 'address', 'type')}),
        ('Permissions', {'fields': ( 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    filter_horizontal = ()
    readonly_fields = ('last_login',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px;" />'.format(obj.image.url))
        return 'No Image'

    image_preview.short_description = 'Image'

# admin.site.register(CustomUser)

# admin.site.register(User)

admin.site.register(Type)

admin.site.register(Member)

admin.site.register(FamilyMember)
