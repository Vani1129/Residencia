from django.db import models
from user.models import Society
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings

class Communication(models.Model):
    TYPE_CHOICES = [
        ('Notice', 'Notice'),
        ('News', 'News'),
        ('Event', 'Event'),
    ]
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='communication')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Notice')
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date = models.DateField(default=timezone.now, null=True, blank=True)
    time = models.TimeField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communication')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_communication')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='communications/documents/', null=True, blank=True)  # Field to attach document
    from_date = models.DateField(null=True, blank=True)  # From date field
    to_date = models.DateField(null=True, blank=True)    # To date field
    
    class Meta:
        verbose_name_plural = "Communication"
    
    def is_valid(self):
        """
        Check if the communication is valid within the from_date and to_date range.
        """
        if self.from_date and self.to_date:
            current_date = timezone.now().date()
            return self.from_date <= current_date <= self.to_date
        return False

# Add custom save method to perform validation
def save(self, *args, **kwargs):
    if self.from_date and self.to_date and self.from_date > self.to_date:
        raise ValueError("from_date cannot be later than to_date")
    super(Communication, self).save(*args, **kwargs)
