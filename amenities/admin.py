from django.contrib import admin
from .models import Amenity

# Register your models here.
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
   list_display = ( 'title', 'description', 'rule_description')
   readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
