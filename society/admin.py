from django.contrib import admin
from .models import Society_profile, Staff

@admin.register(Society_profile)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('society_id', 'society_name', 'city', 'state', 'zip_code')
    search_fields = ( 'society_name__society_name', 'city', 'state', 'zip_code')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'society_name', 'designation', 'joined_date')
    search_fields = ('designation', 'society__society_name__society_name')

# @admin.register(Registration)
# class RegistrationAdmin(admin.ModelAdmin):
#     list_display = ('society_name', 'full_name', 'phone_number', 'email_id', 'type')  # Rep


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'phone_number', 'is_staff', 'is_active',)
#     list_filter = ('email', 'phone_number', 'is_staff', 'is_active',)
#     search_fields = ('email', 'phone_number',)
#     ordering = ('email',)

