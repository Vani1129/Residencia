
from django.contrib import admin
from .models import Visitor,MessageBox, Staff

if not admin.site.is_registered(Visitor):
    
    class VisitorAdmin(admin.ModelAdmin):
        list_display = (
            'first_name', 'last_name', 'visit_date', 
            'check_in_time', 'check_out_time', 'purpose', 
            'approved_by', 'flat_no'
        )
        # readonly_fields = ('created_at', 'updated_at', 'created_by__fullname', 'updated_by__fullname' )


    
class MessageBoxAdmin(admin.ModelAdmin):
    list_display = ( 'created_at', 'updated_at')
    search_fields = ( 'society__name', 'flat_no', 'created_by__fullname', 'updated_by__fullname')  
    # readonly_fields = ('created_at', 'updated_at', 'created_by__fullname', 'updated_by__fullname' )



    def society(self, obj):
        return obj.name.name
    
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(MessageBox, MessageBoxAdmin)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ( 'role', 'joined_date')
    search_fields = ('role', 'society__name')
    # readonly_fields = ('created_at', 'updated_at', 'created_by__fullname', 'updated_by__fullname' )
