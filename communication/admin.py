from django.contrib import admin
from .models import Communication



@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
   list_display = ( 'type', 'title', 'description', 'date')
   # readonly_fields = ('created_at', 'updated_at', 'created_by__fullname', 'updated_by__fullname' )
