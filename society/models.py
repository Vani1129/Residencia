from django.core.validators import RegexValidator
from django.db import models
from user.models import Society
from user.models import UserDetails, User, Type

class Society_profile(models.Model):
    pan_validator = RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$', message='Invalid PAN number format')
    society_id = models.AutoField(primary_key=True)
    society_name = models.ForeignKey(Society, on_delete=models.CASCADE)
    type = models.ManyToManyField(Type)
    
    total_numbers = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=500,null=True, blank=True)
    pan_no = models.CharField(max_length=50,null=True, blank=True)
    gst_no = models.CharField(max_length=50,null=True, blank=True)
    registration_no = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    zip_code = models.CharField(max_length=20,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_societies',null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_societies',null=True, blank=True)

    def __str__(self):
        return f"{self.society_name} ({self.type})"
    
    
class Staff(models.Model):
    society_name = models.ForeignKey(Society_profile, on_delete=models.CASCADE, related_name='staff_members')
    staff_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    joined_date = models.DateField()
    duty_hours_from = models.TimeField()
    duty_hours_to = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='created_staff')
    updated_by = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='updated_staff')

    def __str__(self):
        return f'{self.designation} - {self.society_name.society_name}'