
from django.contrib import admin
from .models import Visitor,MessageBox

if not admin.site.is_registered(Visitor):
    
    class VisitorAdmin(admin.ModelAdmin):
        list_display = (
            'visitor_id', 'first_name', 'last_name', 'visit_date', 
            'check_in_time', 'check_out_time', 'purpose', 
            'approved_by', 'flat_no', 'created_by', 'updated_by'
        )

    
class MessageBoxAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'society_name','created_at', 'updated_at')
    search_fields = ('message_id', 'society__name', 'flat_no', 'created_by__username', 'updated_by__username')  # Assuming 'username' is a field in the user model


    def society(self, obj):
        return obj.society_name.name
    
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(MessageBox, MessageBoxAdmin)
