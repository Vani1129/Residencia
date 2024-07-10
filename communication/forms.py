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
            'from_date': DatePickerInput(format='%Y-%m-%d', options={
                'locale': 'en-us',
                'clearBtn': True,
                'todayBtn': True,
                'todayHighlight': True,
                'autoclose': True,
                'container': '.container-fluid',
            }),
            'to_date': DatePickerInput(format='%Y-%m-%d', options={
                'locale': 'en-us',
                'clearBtn': True,
                'todayBtn': True,
                'todayHighlight': True,
                'autoclose': True,
                'container': '.container-fluid',
            }),
            'time': TimePickerInput(options={
                'locale': 'en-us',
                'clearBtn': True,
                'showMeridian': False,
                'minuteStep': 1,
                'container': '.container-fluid',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'background-color: #f8f9fa; border-color: #ced4da;'

        self.fields['type'].widget.attrs['class'] = 'form-select'
        self.fields['type'].widget.attrs['style'] = 'background-color: #f1f1f1; border-color: #ced4da; color: #495057;'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='form-group col-md-6 mb-3'),
                Column('title', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('date', css_class='form-group col-md-4 mb-3'),
                Column('time', css_class='form-group col-md-4 mb-3'),
                Column('document', css_class='form-group col-md-4 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('from_date', css_class='form-group col-md-6 mb-3'),
                Column('to_date', css_class='form-group col-md-6 mb-3'),
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-3'),
                css_class='form-row',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary')
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
