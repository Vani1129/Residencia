# forms.py
from django import forms
from .models import UserDetails, Member, User, Society, Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from django.urls import reverse_lazy

class UserDetailsForm(forms.ModelForm):
    number_of_members = forms.IntegerField(min_value=1, label="Number of Members", required=True, initial=1)

    class Meta:
        model = UserDetails
        fields = '__all__'


class MemberForm(forms.ModelForm):
    society_name = forms.CharField(max_length=255, required=True)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label="User")
    flat_number = forms.ModelChoiceField(queryset=UserDetails.objects.values_list('flat_number', flat=True), required=True, label="Flat Number")
    number_of_members = forms.IntegerField(min_value=1, label="Number of Members")

    class Meta:
        model = Member
        fields = ['society', 'user', 'flat_number', 'member_name', 'phone_no', 'age', 'created_at', 'updated_at']
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['society'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        number_of_members = cleaned_data.get('number_of_members')
        if number_of_members:
            cleaned_data['number_of_members'] = number_of_members
        return cleaned_data


class UserForm(forms.ModelForm):
    society_name = forms.ModelChoiceField(
        queryset=Society.objects.all(),
        required=True,
        label='Society',
        widget=forms.Select
    )
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'image', 'society_name', 'address', 'type']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'society_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Applying CSS classes to fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        # Creating a form helper for layout customization
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('image', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('society_name', css_class='form-group col-md-6 mb-3'),
                Column('address', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('type', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class OTPForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    otp = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255, required=True)
    otp = forms.CharField(max_length=6, required=True)

from django.urls import reverse_lazy


class SocietyForm(forms.ModelForm):
    

    society_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget= forms.CheckboxSelectMultiple
    )
    is_active = forms.BooleanField(label='Active', required=False)

    class Meta:
        model = Society
        fields = ['society_name', 'type', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Creating a form helper for layout customization
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('society_name', css_class='form-group col-md-6 mb-3'),
                Column('description', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('type', css_class='form-group col-md-12 mb-3'),
                Column('is_active', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary'),
                    HTML('<a href="%s" class="btn btn-secondary ml-2">Back to Societies List</a>' % reverse_lazy('show_societies')),
                    css_class='form-group col-md-12 mb-3'
                ),
                css_class='form-row',
            )
        )


class SubadminForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    phone_no = forms.CharField(max_length=15)
    email = forms.EmailField(required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = UserDetails
        fields = ['name', 'role', 'email', 'phone_no', 'flat_number', 'flat_type']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'image'] 
        