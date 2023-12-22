from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', include(('apps.accounts.urls', 'account'), namespace='account')),  # Removed the 'r'^' as it's not required
    path('travel/', include(('apps.destinations.urls', 'travel'), namespace='travel')),  # Removed the 'r'^' as it's not required
    path('logout/', LogoutView.as_view(), name='logout'),  # Removed the 'r'^' as it's not required
    path('admin/', admin.site.urls),  # Removed the 'r'^' as it's not required
]

if settings.DEBUG:  # If it is in debug mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Concatenate the static URLs correctly
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Concatenate the static URLs correctly

