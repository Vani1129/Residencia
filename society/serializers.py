from rest_framework import serializers
from .models import Societyprofile

class SocietyProfileSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='name.name', read_only=True)
    society_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Societyprofile
        fields = [
            'name_display',
            'society_type_display',
            'total_numbers',
            'address',
            'pan_no',
            'gst_no',
            'registration_no',
            'city',
            'state',
            'zip_code',
        ]

    def get_society_type_display(self, obj):
        return ', '.join([str(t) for t in obj.name.type.all()])