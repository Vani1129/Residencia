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


class UserForm(forms.ModelForm):
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
        model = User
        fields = ['full_name', 'email', 'phone_number', 'image']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            # 'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

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
                Column('full_name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('image', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
         
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class OTPForm(forms.Form):
    phone_number = forms.CharField(max_length=10)
    otp = forms.CharField(label='OTP', max_length=6)


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255, required=True)
    otp = forms.CharField(max_length=6, required=True)


class SocietyForm(forms.ModelForm):
    society_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget=forms.CheckboxSelectMultiple
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
                css_class='form-row',
            ),
            Row(
                Column('type', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Row(
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
        fields = ['name', 'role', 'email', 'phone_no', 'flat_number']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'image'] 
        
        
class MemberForm(forms.ModelForm):
    society_name_display = forms.CharField(
        label='Society Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    
    society_name = forms.CharField(label="Society Name", max_length=100,required=False)
    building = forms.CharField(label="Building Name", max_length=100,required=False)
    flat_number = forms.CharField(label="Flat Number", max_length=10,required=False)
    full_name = forms.CharField(label="Full Name", max_length=100,required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female')],required=False)
    email = forms.EmailField(label="Email",required=False)
    phone_number = forms.CharField(label="Phone Number", max_length=15,required=False)
    country = forms.CharField(label="Country", max_length=100,required=False)
    address = forms.CharField(label="Address", max_length=100,required=False)
    image = forms.ImageField(label="Image", required=False)
    member_type = forms.ChoiceField(label="Member Type", choices=[('R', 'Resident'), ('O', 'Owner')],required=False)
    number_of_members = forms.IntegerField(label="Number of Members",required=False)
    class Meta:
        model = Member
        fields = (
            'society_name', 'building', 'flat_number', 'full_name','date_of_birth','gender','email','phone_number','country','address','image','member_type','number_of_members',
        )
       
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.society:
            self.fields['society_name'].initial = instance.society.society_name.society_name

class FamilyMemberForm(forms.Form):
    family_full_name = forms.CharField(max_length=50, required=False)
    family_date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    family_gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    family_phone_number = forms.CharField(max_length=20, required=False)
    family_type = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        number_of_members = cleaned_data.get('number_of_members')
        if number_of_members:
            cleaned_data['number_of_members'] = number_of_members
        return cleaned_data
