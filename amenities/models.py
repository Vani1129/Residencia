from django.db import models
from django.conf import settings
from society.models import Society_profile

class Amenity(models.Model):
    society_id = models.ForeignKey(Society_profile, on_delete=models.CASCADE, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to='media/amenities', blank=True, null=True)  
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rule_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='amenities_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='amenities_updated_by')

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.title
