from django import forms
from .models import Societyprofile
from .models import Building
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError

from django import forms
from .models import Societyprofile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class SocietyprofileForm(forms.ModelForm):
    name_display = forms.CharField(
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
        model = Societyprofile
        fields = [
            'name_display',
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
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name_display', css_class='form-group col-md-6 mb-3'),
                Column('society_type_display', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
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
        return self.instance.type.all()

     
class OTPForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    otp = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)






class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'total_flats', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_flats': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'total_flats': 'Number of Flats',
        }

    def clean_total_flats(self):
        total_flats = self.cleaned_data.get('total_flats')
        if total_flats is None or total_flats < 1:
            raise forms.ValidationError("Please enter a valid number of flats (minimum 1).")
        return total_flats    
    

