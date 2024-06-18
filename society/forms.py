from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['full_name','email', 'phone_number','society_name','type','password', 'address']
        
class OTPForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    otp = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)