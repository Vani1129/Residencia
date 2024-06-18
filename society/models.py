from django.core.validators import RegexValidator
from django.db import models
# from django.contrib.auth.models import BaseUserManager
from user.models import UserDetails


# class UserManager(BaseUserManager):
#     def create_user(self, email, phone_number, society_name, type, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         if not phone_number:
#             raise ValueError('The Phone Number field must be set')
#         if not society_name:
#             raise ValueError('The Society Name field must be set')
#         if not type:
#             raise ValueError('The Type field must be set')
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, phone_number=phone_number, society_name=society_name, type=type, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, phone_number, society_name, type, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, phone_number, society_name, type, password, **extra_fields)

# class User(AbstractBaseUser):
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     society_name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     TYPE_CHOICES = [
#         ('bungalow', 'Bungalow'),
#         ('flat', 'Flat'),
#         ('rowhouse', 'Rowhouse'),
#     ]
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['phone_number', 'society_name', 'type']

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
    
#     def __str__(self):
#         return self.email

# class Registration(models.Model):
#     society_name = models.CharField(max_length=255)
#     full_name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=20)
#     address = models.CharField(max_length=500)
#     email = models.EmailField(max_length=255)  # Changed field name
#     TYPE_CHOICES = [
#         ('bungalow', 'Bungalow'),
#         ('flat', 'Flat'),
#         ('rowhouse', 'Rowhouse'),
#     ]
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES)

#     def __str__(self):
#         return self.full_name

class Society(models.Model):
    pan_validator = RegexValidator(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$', message='Invalid PAN number format')

    society_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    #society_name = models.ForeignKey(User, on_delete=models.CASCADE)
    society_name = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    
    TYPE_CHOICES = [
        ('bungalow', 'Bungalow'),
        ('flat', 'Flat'),
        ('rowhouse', 'Rowhouse'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    total_numbers = models.IntegerField()
    address = models.CharField(max_length=500)
    pan_no = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='created_societies')
    updated_by = models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name='updated_societies')

    def __str__(self):
        return self.name

class Staff(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
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
        return f'{self.designation} - {self.society}'
