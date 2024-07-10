from django.core.validators import RegexValidator
from django.db import models
from user.models import Society, Type
from user.models import  User
from django.conf import settings  


class Societyprofile(models.Model):
    pan_validator = RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$', message='Invalid PAN number format')
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='societyprofile')
    name= models.CharField(max_length=50)
    total_numbers = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=500,null=True, blank=True)
    pan_no = models.CharField(max_length=10,null=True, blank=True)
    gst_no = models.CharField(max_length=10,null=True, blank=True)
    registration_no = models.CharField(max_length=10,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    zip_code = models.CharField(max_length=20,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_societies',null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_societies',null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    

class Building(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=50,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    total_flats = models.PositiveIntegerField(verbose_name="Number of Flats",default=0)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_building')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_building')

    def __str__(self):
        return self.name

