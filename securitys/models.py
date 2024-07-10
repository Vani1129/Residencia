# models.py
from django.db import models
from django.conf import settings  
from society.models import Societyprofile 
from user.models import Member, Society, User

class Visitor(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='visitor')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    visit_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    purpose = models.CharField(max_length=255)
    approved_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_visitor')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_visitor')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MessageBox(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='message_boxes')
    message = models.TextField()
    flat_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_messages')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_messages')

    def __str__(self):
        return f'Message {self.message_id} for Society {self.name.name}'



class Staff(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='staff_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    joined_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2) 
    duty_hours_from = models.TimeField()
    duty_hours_to = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_staff')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_staff')

    def __str__(self):
        return self.name
    