from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from .forms import TripForm
from .models import Destination

User = get_user_model()

class HomeView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'account:home'
    template_name = 'destinations/dashboard.html'

    def get_context_data(self, **kwargs):
        obj_list = super(HomeView, self).get_context_data(**kwargs)
        qs = Destination.objects.all()
        user_results = qs.filter(users_on_trip=self.request.user)
        others_trips = qs.exclude(users_on_trip=self.request.user)
        obj_list['user_trips'] = user_results
        obj_list['other_users_trips'] = others_trips
        return obj_list