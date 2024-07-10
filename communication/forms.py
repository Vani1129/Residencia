from django import forms
from .models import Communication
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django.utils import timezone

class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ['type', 'title', 'description', 'date', 'time', 'document', 'from_date', 'to_date']
        widgets = {
            'date': DatePickerInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f8f9fa;'
            }),
            'time': TimePickerInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f8f9fa;',
                'data-toggle': 'datetimepicker', 
                'data-target': '#id_time'
            }),
            'from_date': DatePickerInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f8f9fa;'
            }),
            'to_date': DatePickerInput(attrs={
                'class': 'form-control', 
                'style': 'background-color: #f8f9fa;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Applying CSS classes and styles to fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'background-color: #f8f9fa; border-color: #ced4da;'

        # Assigning a specific class and style to the 'type' field
        self.fields['type'].widget.attrs['class'] = 'form-select'
        self.fields['type'].widget.attrs['style'] = 'background-color: #f1f1f1; border-color: #ced4da; color: #495057;'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='form-group col-md-6 mb-3', style='padding: 10px; background-color: #ffffff;'),
                Column('title', css_class='form-group col-md-6 mb-3', style='padding: 10px; background-color: #ffffff;'),
                css_class='form-row',
            ),
            Row(
                Column('date', css_class='form-group col-md-4 mb-3', style='padding: 10px; background-color: #ffffff;'),
                # Column('time', css_class='form-group col-md-4 mb-3', style='padding: 10px; background-color: #ffffff;'),
                Column('document', css_class='form-group col-md-4 mb-3', style='padding: 10px; background-color: #ffffff;'),
                css_class='form-row',
            ),
            Row(
                Column('from_date', css_class='form-group col-md-6 mb-3', style='padding: 10px; background-color: #ffffff;'),
                Column('to_date', css_class='form-group col-md-6 mb-3', style='padding: 10px; background-color: #ffffff;'),
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3', style='padding: 10px; background-color: #ffffff;'),
                css_class='form-row',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary', style='background-color: #007bff; border-color: #007bff; color: #ffffff; padding: 10px 20px;')
        )

    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.now().date()

        if date < today:
            raise forms.ValidationError("Date cannot be in the past.")
        elif date > today:
            raise forms.ValidationError("Date cannot be in the future.")

        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        current_time = timezone.now().time()

        if time != current_time:
            raise forms.ValidationError("Please select the current time.")

        return time

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("from_date cannot be later than to_date")

        return cleaned_data
