# models.py
from django.db import models
from django.conf import settings  
from society.models import Society_profile 
from user.models import Member  

class Visitor(models.Model):
    visitor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    visit_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    purpose = models.CharField(max_length=255)
    approved_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    flat_no = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MessageBox(models.Model):
    society_name = models.ForeignKey(Society_profile, on_delete=models.CASCADE, related_name='message_boxes')
    message_id = models.AutoField(primary_key=True)
   # member_name = models.CharField(max_length=255)
    message = models.TextField()
    flat_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_messages')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_messages')

    def __str__(self):
        return f'Message {self.message_id} for Society_profile {self.society_name.name}'
