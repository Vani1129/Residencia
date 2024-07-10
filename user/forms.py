# forms.py
from django import forms
from .models import FamilyMember, UserDetails, Member, User, Society, Type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.forms import ValidationError
from django.utils import timezone
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from django.utils.safestring import mark_safe


class UserDetailsForm(forms.ModelForm):
    number_of_members = forms.IntegerField(min_value=1, label="Number of Members", required=True, initial=1)

    class Meta:
        model = UserDetails
        fields = '__all__'




class UserForm(forms.ModelForm):
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
        model = User
        fields = ['fullname', 'email', 'phone_number', 'image']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name_display', css_class='form-group col-md-6 mb-3'),
                Column('society_type_display', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('fullname', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('image', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column( Submit('submit', 'Submit', css_class='btn btn-primary'), ),
                css_class='form-row',
            )
        )


class OTPForm(forms.Form):
    phone_number = forms.CharField(max_length=10)
    otp = forms.CharField(label='OTP', max_length=6,initial='999000')


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255, required=True)
    otp = forms.CharField(max_length=6, required=True)


class SocietyForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_from_date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_to_date'}), required=False)
    interval = forms.ChoiceField(
        choices=Society.INTERVAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_interval'}),
        required=False,
    )

    class Meta:
        model = Society
        fields = ['name', 'type', 'from_date', 'to_date', 'interval']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Form fields:", self.fields)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('name', css_class='form-group col-md-6 mb-3'),
                        Column('type', css_class='form-group col-md-12 mb-3'),
                        css_class='form-row'
                    ),
                    css_class='col-md-12'
                ),
                Column(
                    Row(
                        Column('interval', css_class='form-group col-md-4 mb-3'),
                        Column('from_date', css_class='form-group col-md-4 mb-3'),
                        Column('to_date', css_class='form-group col-md-4 mb-3'),
                        css_class='form-row'
                    ),
                    css_class='col-md-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary'),
                    HTML('<a href="%s" class="btn btn-secondary ml-2">Back to Societies List</a>' % reverse_lazy('show_societies')),
                    css_class='form-group col-md-12 mb-3'
                ),
                css_class='form-row',
            ),
            HTML(
                mark_safe(
                    """
                    <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const intervalSelect = document.getElementById('id_interval');
                        const fromDateInput = document.getElementById('id_from_date');
                        const toDateInput = document.getElementById('id_to_date');

                        function calculateToDate() {
                            const fromDate = new Date(fromDateInput.value);
                            const interval = intervalSelect.value;
                            
                            if (fromDate && interval) {
                                let toDate;
                                switch (interval) {
                                    case 'monthly':
                                        toDate = new Date(fromDate.setMonth(fromDate.getMonth() + 1));
                                        break;
                                    case 'quarterly':
                                        toDate = new Date(fromDate.setMonth(fromDate.getMonth() + 3));
                                        break;
                                    case 'yearly':
                                        toDate = new Date(fromDate.setFullYear(fromDate.getFullYear() + 1));
                                        break;
                                    default:
                                        toDate = '';
                                }
                                toDateInput.value = toDate ? toDate.toISOString().split('T')[0] : '';
                            }
                        }

                        intervalSelect.addEventListener('change', calculateToDate);
                        fromDateInput.addEventListener('change', calculateToDate);
                    });
                    </script>
                    """
                )
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        interval = cleaned_data.get('interval')

        if from_date and interval:
            if interval not in dict(Society.INTERVAL_CHOICES).keys():
                raise ValidationError('Invalid interval selected.')

            if interval == 'monthly':
                cleaned_data['to_date'] = from_date + relativedelta(months=1)
            elif interval == 'quarterly':
                cleaned_data['to_date'] = from_date + relativedelta(months=3)
            elif interval == 'yearly':
                cleaned_data['to_date'] = from_date + relativedelta(years=1)
            else:
                raise ValidationError('Invalid interval provided.')

        return cleaned_data

def validate_from_date(value):
    if value < timezone.now().date():
        raise ValidationError('From date cannot be in the past.')

def validate_to_date(value):
    if value < timezone.now().date():
        raise ValidationError('To date cannot be in the past.')

    # def _init_(self, *args, **kwargs):
    #     super()._init_(*args, **kwargs)

    #     # Creating a form helper for layout customization
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('name', css_class='form-group col-md-6 mb-3'),
    #             css_class='form-row',
    #         ),
    #         Row(
    #             Column('type', css_class='form-group col-md-12 mb-3'),
    #             css_class='form-row',
    #         ),
    #         Row(
    #             Column('from_date', css_class='form-group col-md-6 mb-3'),
    #             Column('interval', css_class='form-group col-md-6 mb-3'),
    #             css_class='form-row',
    #         ),
    #         Row(
    #             Column('to_date', css_class='form-group col-md-6 mb-3'),
    #             css_class='form-row',
    #         ),
    #         Row(
    #             Column(
    #                 Submit('submit', 'Submit', css_class='btn btn-primary'),
    #                 HTML('<a href="%s" class="btn btn-secondary ml-2">Back to Societies List</a>' % reverse_lazy('show_societies')),
    #                 css_class='form-group col-md-12 mb-3'
    #             ),
    #             css_class='form-row',
    #         )
    #     )

   
class SubadminForm(forms.ModelForm):
    name = forms.CharField(label="Full Name", max_length=100, required=True)
    phone_no = forms.CharField(label="Phone Number", max_length=10, required=True)
    email = forms.EmailField(label="Email", required=False)
    flat_number = forms.CharField(label="Flat Number", max_length=10, required=True)
    # flat_type = forms.CharField(label="Flat Type", max_length=50, required=True)
    role = forms.ChoiceField(
        label="Role",
        choices=(
            # ('resident', 'Resident'),
            ('committee_member', 'Committee Member'),
        ),
        required=True
    )

    class Meta:
        model = UserDetails
        fields = ['name', 'role', 'email', 'phone_no', 'flat_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('role', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone_no', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('flat_number', css_class='form-group col-md-6 mb-3'),
                # Column('flat_type', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column(
                    Submit('submit', 'Submit', css_class='btn btn-primary'),
                    ),
                css_class='form-row',
            )
        )

        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'fullname', 'phone_number', 'image'] 
        
        

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Member, FamilyMember

class MemberForm(forms.ModelForm):
    name_display = forms.CharField(
        label='Society Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    building_display = forms.CharField(
        label='Building Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    flat_number = forms.CharField(label="Flat Number", max_length=10, required=True)
    fullname = forms.CharField(label="Full Name", max_length=100, required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(label="Gender", choices=[('M', 'Male'), ('F', 'Female')], required=False)
    email = forms.EmailField(label="Email", required=False)
    phone_number = forms.CharField(label="Phone Number", max_length=10, required=False)
    image = forms.ImageField(label="Image", required=False)
    member_type = forms.ChoiceField(label="Member Type", choices=[('R', 'Resident'), ('O', 'Owner')], required=False)
    number_of_members = forms.IntegerField(label="Number of Members", required=False)

    class Meta:
        model = Member
        fields = (
            'name_display', 'building_display', 'flat_number', 'fullname', 'date_of_birth',
            'gender', 'email', 'phone_number', 'image', 'member_type', 'number_of_members',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name_display', css_class='form-group col-md-6 mb-3'),
                Column('building_display', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('flat_number', css_class='form-group col-md-6 mb-3'),
                Column('fullname', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-6 mb-3'),
                Column('gender', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-3'),
                Column('member_type', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('number_of_members', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
        )

  
class FamilyMemberForm(forms.ModelForm):
    family_fullname = forms.CharField(max_length=50, required=False)
    family_date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    family_gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    family_phone_number = forms.CharField(max_length=10, required=False)
    family_relation = forms.CharField(max_length=50, required=False)

    class Meta:
        model = FamilyMember
        fields = (
            'family_fullname', 'family_date_of_birth', 'family_gender', 'family_relation', 'family_phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('family_fullname', css_class='form-group col-md-6 mb-3'),
                Column('family_date_of_birth', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('family_gender', css_class='form-group col-md-6 mb-3'),
                Column('family_phone_number', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('family_relation', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
        )


FamilyMemberFormSet = forms.modelformset_factory(
    FamilyMember,
    form=FamilyMemberForm,
    extra=1,
    can_delete=True
)
