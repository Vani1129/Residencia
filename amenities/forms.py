from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Amenity
from user.models import Society

class AmenityForm(forms.ModelForm):
    
    name_display = forms.CharField(
        label='Society Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Amenity
        fields = ['name_display', 'title', 'description', 'rule_description', 'images', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'rule_description': forms.Textarea(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            # 'from_date': DatePickerInput(attrs={'class': 'form-control'}),
            # 'to_date': DatePickerInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            self.fields['name_display'].initial = instance.society.name  # Fixed this line to use the society name

        # Applying CSS classes to fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Creating a form helper for layout customization
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name_display', css_class='form-group col-md-6 mb-3'),
                Column('title', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('rule_description', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('images', css_class='form-group col-md-6 mb-3'),
                Column('document', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            # Row(
            #     Column('from_date', css_class='form-group col-md-6 mb-3'),
            #     Column('to_date', css_class='form-group col-md-6 mb-3'),
            #     css_class='form-row',
            # ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     from_date = cleaned_data.get('from_date')
    #     to_date = cleaned_data.get('to_date')

    #     if from_date and to_date and from_date > to_date:
    #         raise forms.ValidationError("From date cannot be later than to date")

    #     return cleaned_data
