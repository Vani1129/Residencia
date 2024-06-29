from django import forms
from user.models import User
from .models import Society_profile
from .models import Building, Unit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError


class SocietyProfileForm(forms.ModelForm):
    society_name_display = forms.CharField(
        label='Society Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    society_type_display = forms.CharField(
        label='Society Type',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Society_profile
        fields = [
            'society_name_display',
            'society_type_display',
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
        super().__init__(*args, **kwargs)
        # Initialize the crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('society_name_display', css_class='form-group col-md-6 mb-3'),
                Column('society_type_display', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                # Column('total_numbers', css_class='form-group col-md-6 mb-3'),
                Column('address', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('state', css_class='form-group col-md-6 mb-3'),
                Column('zip_code', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-3'),
                Column('registration_no', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            
             Row(
                Column('pan_no', css_class='form-group col-md-6 mb-3'),
                Column('gst_no', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


    def clean_type(self):
        # Ensure type data is not changed
        return self.instance.type.all()


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




class BuildingForm(forms.ModelForm):
    society_name_display = forms.CharField(
        label='Society Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Building
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(BuildingForm, self).__init__(*args, **kwargs)
        if instance and instance.society:
            self.fields['society_name_display'].initial = instance.society.society.society_name

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Building.objects.filter(name=name).exists():
            raise ValidationError("Building with this Name already exists.", code='unique')
        return name
    
    

class UnitForm(forms.ModelForm):
    building_name_display = forms.CharField(
        label='Building Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Unit
        fields = ['unit_number', 'unit_type', 'area']
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_type': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.building:
            self.fields['building_name_display'].initial = instance.building.name
