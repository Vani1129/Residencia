from django.db import models
from django.conf import settings
from user.models import Society, User

class Amenity(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='amenities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to='media/amenities', blank=True, null=True)  
    document = models.FileField(upload_to='media/amenity_documents', blank=True, null=True)  # New field for attaching documents
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
