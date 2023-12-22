# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import logging
from django.http import JsonResponse

class Countries(TemplateView): 

    def get(self, request, *args, **kwargs):
        # Configure logging settings (you can adjust the level, format, and handlers as needed)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        countries_list = []
        api_url = "https://restcountries.com/v3.1/all?fields=name"

        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the response is successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and log country names
            for country in data:
                c = country.get('name', {}).get('common')
                if c:
                    countries_list.append(c)
                    #logging.info(f'Country: {c} added to the list.')
        else:
            # Log an error message for unsuccessful response
            logging.error(f'Error making API request. Status code: {response.status_code}')

        return render(request, 'destinations/countries.html', context={'places': countries_list})
    
def ajax_endpoint(request):
    # Perform any data fetching or processing here
    # For example, you can make a request to the specified API endpoint
    api_url = "https://restcountries.com/v3.1/independent?status=true"
    response = requests.get(api_url)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if response.status_code == 200:
        data_ajax = response.json()
        logging.info(data_ajax)
        return JsonResponse({'result': data_ajax})
    else:
        return JsonResponse({'error': 'Error making API request'}, status=500)

