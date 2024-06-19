from django import forms
from user.models import User
from .models import Society_profile


class SocietyProfileForm(forms.ModelForm):
    society_name_display = forms.CharField(label='Society Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    
    class Meta:
        model = Society_profile
        fields = [
            
            'type',
            'total_numbers',
            'address',
            'pan_no',
            'gst_no',
            'registration_no',
            'city',
            'state',
            'zip_code',
        ]
        widgets = {
            # 'society_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'type': forms.SelectMultiple(attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'}),
            'total_numbers': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_no': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SocietyProfileForm, self).__init__(*args, **kwargs)
        # self.fields['society_name'].disabled = True 
       
        self.fields['society_name_display'].initial = self.instance.society_name.society_name
        self.fields['type'].disabled = True  # Ensure the type field is disabled

    # def __init__(self, *args, **kwargs):
    #     super(SocietyProfileForm, self).__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['society_name_display'].initial = self.instance.society_name.name
    #         self.fields['type_display'].initial = ', '.join([str(type) for type in self.instance.type.all()])

    
    def clean_type(self):
        # Ensure type data is not changed
        return self.instance.type.all()
    
# class SocietyProfileForm(forms.ModelForm):
#     society_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
#     type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

#     class Meta:
#         model = Society_profile
#         fields = [
#             'society_name',
#             'type',
#             'total_numbers',
#             'address',
#             'pan_no',
#             'gst_no',
#             'registration_no',
#             'city',
#             'state',
#             'zip_code',
#         ]
#         widgets = {
#             'total_numbers': forms.NumberInput(attrs={'class': 'form-control'}),
#             'address': forms.TextInput(attrs={'class': 'form-control'}),
#             'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
#             'gst_no': forms.TextInput(attrs={'class': 'form-control'}),
#             'registration_no': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'state': forms.TextInput(attrs={'class': 'form-control'}),
#             'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(SocietyProfileForm, self).__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['society_name'].initial = self.instance.society_name
#             self.fields['type'].initial = ", ".join([str(t) for t in self.instance.type.all()])

        
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