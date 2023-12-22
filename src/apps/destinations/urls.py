from django.urls import include, path
from .api_views import Countries,ajax_endpoint
from .views import UpdateDestinationRatingView
from .views import UpdateDestinationView, HomeView, AddDestinationFormView, DestinationDetailSlugView


urlpatterns = [
    path('dashboard/', HomeView.as_view(), name='home'),
    path('destination/add/', AddDestinationFormView.as_view(), name='add_trip'),
    path('destination/update/', UpdateDestinationView, name='destination_update'),
    path('destination/<slug:slug>/', DestinationDetailSlugView.as_view(), name='detail'),
    path('update_rating/<int:destination_id>/', UpdateDestinationRatingView.as_view(), name='update_rating'),
    path('countries/', Countries.as_view(), name='countries_list'),
    path('ajax_endpoint/', ajax_endpoint, name='ajax_endpoint'),
]