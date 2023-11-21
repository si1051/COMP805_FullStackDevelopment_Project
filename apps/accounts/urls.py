from django.urls import include, path
from .views import register_view, LoginFormView

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('register/', register_view, name='register'),
]
