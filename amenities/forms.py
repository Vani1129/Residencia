from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Amenity

class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['title', 'description', 'rule_description', 'images']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'rule_description': forms.Textarea(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Applying CSS classes to fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Creating a form helper for layout customization
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'  # Ensuring the form takes full width
        self.helper.label_class = 'col-md-3 col-form-label'  # Adjusting label width
        self.helper.field_class = 'col-md-9'  # Adjusting field width

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='mb-3', style='padding: 10px; border-color: #ced4da;'),  # Adjusting column width and removing background color
                css_class='form-row',
            ),
            Row(
                Column('description', css_class='mb-3', style='padding: 10px; border-color: #ced4da;'),  # Adjusting column width and removing background color
                css_class='form-row',
            ),
            Row(
                Column('rule_description', css_class='mb-3', style='padding: 10px; border-color: #ced4da;'),  # Adjusting column width and removing background color
                css_class='form-row',
            ),
            Row(
                Column('images', css_class='mb-3', style='padding: 10px; border-color: #ced4da;'),  # Adjusting column width and removing background color
                css_class='form-row',
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary', style='background-color: #007bff; border-color: #007bff; color: #ffffff; padding: 10px 20px;')  # Submit button with custom color and padding
        )
