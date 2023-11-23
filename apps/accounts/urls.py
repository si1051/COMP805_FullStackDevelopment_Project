from django.contrib import admin
from django.urls import include, path
from .views import register_view, LoginFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appname/', include('appname.urls')),
    path('', LoginFormView.as_view(), name='login'),
    path('register/', register_view, name='register'),
]

