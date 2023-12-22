# apps/destinations/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import TripForm
from ..models import Destination

@login_required
def destination_add(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            destination = Destination.objects.new(form.cleaned_data, user=request.user)
            return redirect('some_success_url')  # Redirect to a success page
    else:
        form = TripForm()
    return render(request, 'destination_add.html', {'form': form})

@login_required
def destination_update_rating(request, destination_id):
    if request.method == 'POST':
        new_rating = request.POST.get('new_rating')
        destination = Destination.objects.get(pk=destination_id)
        destination.rating = new_rating
        destination.save()
        return redirect('some_success_url')  # Redirect to a success page
    else:
        # Handle GET request if needed
        pass
