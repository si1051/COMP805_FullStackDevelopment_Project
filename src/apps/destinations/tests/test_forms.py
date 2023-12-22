# apps/destinations/forms.py
from django import forms
from django.utils import timezone

class TripForm(forms.ModelForm):
    # ... (other fields and methods)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            now = timezone.now().date()

            if end_date < now:
                raise forms.ValidationError("End date cannot be in the past.")

            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before the start date.")

        return cleaned_data
