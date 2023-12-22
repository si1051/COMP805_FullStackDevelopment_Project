from django import forms
from django.contrib.auth import get_user_model
import datetime
import pytz
import requests
from django.utils import timezone


now = timezone.now()

User = get_user_model()

class TripForm(forms.Form):
    name = forms.CharField(label="Trip Name", widget=forms.TextInput(
        attrs={"class": "form-control", 'id': 'form_name', "placeholder": "Give your trip a name", }))
    
    location = forms.ChoiceField(
        label="Destination",
        choices=[],
        widget=forms.Select(attrs={"class": "form-control", 'id': 'form_location'})
    )
    
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'form_description', 'rows': '3'}))
    
    start_date = forms.DateTimeField(label='Start Date', widget=forms.DateTimeInput(
        attrs={'type': 'date', 'class': 'form-control', 'id': 'form_start_date'}))
    
    end_date = forms.DateTimeField(label="End Date", widget=forms.DateInput(
        attrs={'type': 'date', "class": "form-control", 'id': 'form_end_date'}))
    
    rating = forms.IntegerField(label="Rating", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'form_rating', 'min': '0', 'max': '5'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the list of countries and populate choices for the location field
        self.fields['location'].choices = self.get_countries_list()

    def get_countries_list(self):
        countries_list = []

        # API endpoint for countries
        api_url = "https://restcountries.com/v3.1/all?fields=name"

        # Make a GET request to the API
        try:
            response = requests.get(api_url)

            # Check if the response is successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Extract country names and add to the list
                for country in data:
                    c = country.get('name', {}).get('common')
                    if c:
                        countries_list.append((c, c))  # Use the country name as both the display and value
            else:
                # Log an error message for unsuccessful response
                countries_list.append(('Error', 'Error fetching countries'))
        except requests.RequestException as e:
            # Handle the exception more gracefully, e.g., log it or provide a default option
            countries_list.append(('Error', 'Error fetching countries'))

        return countries_list

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        location = cleaned_data.get('location')
        description = cleaned_data.get('description')
        start_date = cleaned_data.get('start_date')

        # Handle the case when end_date is None more gracefully
        end_date = cleaned_data.get('end_date')
        if end_date:
            end_date = end_date.replace(tzinfo=None)

        rating = cleaned_data.get('rating', None)

        if rating is not None and (rating < 0 or rating > 5):
            msg = 'Rating must be between 0 and 5'
            self.add_error('rating', msg)

        if not name:
            msg = 'Please provide a name for your trip'
            self.add_error('name', msg)
        if not location:
            msg = 'Please provide a location'
            self.add_error('location', msg)
        if not description:
            msg = 'No description was provided'
            self.add_error('description', msg)
        if start_date and start_date < now:
            msg = 'Start date must be in the future'
            self.add_error('start_date', msg)
        if end_date and end_date < now:
            msg = 'End date must be in the future'
            self.add_error('end_date', msg)
        if end_date and start_date and end_date < start_date:
            msg = 'End date must be after start date'
            self.add_error('end_date', msg)

        return cleaned_data
