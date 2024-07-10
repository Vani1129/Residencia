from django.contrib import admin
from .models import Societyprofile, Building

@admin.register(Societyprofile)
class SocietyprofileAdmin(admin.ModelAdmin):
    list_display = ( 'city', 'state', 'zip_code')
    search_fields = ( 'name__name', 'city', 'state', 'zip_code')



admin.site.register(Building)

# @admin.register(Building)
# class BuildingAdmin(admin.ModelAdmin):
    # list_display = (  'name')
    # search_fields = ('name', 'name__name')
    # readonly_fields = ('created_at', 'updated_at', 'created_by__fullname', 'updated_by__fullname' )



