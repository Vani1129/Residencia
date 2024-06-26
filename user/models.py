from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from datetime import datetime, timedelta

class Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, full_name, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(None, email, phone_number, password, **extra_fields)
    
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True,null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True,null=True, blank=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    society_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    TYPE_CHOICES = [
        ('bungalow', 'Bungalow'),
        ('flat', 'Flat'),
        ('rowhouse', 'Rowhouse'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.email
    
# models.py
from django.db import models
from django.utils import timezone

class Society(models.Model):
    society_name = models.CharField(max_length=255)
    type = models.ManyToManyField(Type, related_name="society_type")
    is_active = models.BooleanField()
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(null=True, blank=True)
    from_time = models.TimeField(default=timezone.now)
    to_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.society_name

class UserDetails(models.Model):
    society_sub = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='society_subadmin',null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userdetails")
    # name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=(
        ('resident', 'Resident'),
        ('committee_member', 'Committee Member'),
    ))
    flat_number = models.CharField(max_length=20)
    flat_type = models.CharField(max_length=20, choices=(
        ('bungalow', 'Bungalow'),
        ('flat', 'Flat'),
        ('rowhouse', 'Rowhouse')
    ))
    area = models.CharField(max_length=255, null=True)
    move_in_date = models.DateField(null=True)
    move_out_date = models.DateField(null=True, blank=True)
    # phone_no = models.CharField(max_length=10, null=True)
    age = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name 
    
    
class Member(models.Model):
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    building = models.CharField(max_length=100,null=True, blank=True)
    flat_number = models.CharField(max_length=20,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES )
    country = models.CharField(max_length=5, null=True, blank=True)
    member_type = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Member: {self.user.full_name} ({self.user.email})"

class FamilyMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='family_members')
    full_name = models.CharField(max_length=50,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    family_relation = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return f"Family Member: {self.full_name} of {self.member.full_name}"
    
    

    
    
    
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)

    def set_otp(self, otp):
        self.otp = otp
        self.otp_expiration = datetime.now() + timedelta(minutes=10)  # OTP valid for 10 minutes
        self.save()

    def check_otp(self, otp):
        if self.otp == otp and datetime.now() <= self.otp_expiration:
            self.otp = None  # Clear OTP after successful verification
            self.save()
            return True
        return False
    


class Society_profile(models.Model):
    society_name = models.OneToOneField(Society, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"Profile of {self.society_name}"
    
    
