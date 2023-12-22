from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.generic import TemplateView
from .forms import LoginForm, RegisterForm

User = get_user_model()

class LoginFormView(TemplateView):
    form_class = LoginForm
    initial = {'key': 'value'}
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('travel:home')
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                if user is not None:
                    login(request, user)
                    response_data = {'msg': 'Logged in! Good to go!'}
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                else:
                    errors = {'non_field_errors': ['Invalid Credentials']}
                    return HttpResponse(json.dumps(errors), status=403, content_type="application/json")

            if user is not None:
                login(request, user)
                return redirect('travel:home')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('account:login')
        return render(request, self.template_name, {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('travel:home')
    else:
        form = RegisterForm(request.POST or None)
        context = {'form': form}

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            newUser = User.objects.create_user(username, email, password)

            if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                response_data = {'msg': 'Good to go!'}
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

        return render(request, "accounts/register.html", context)

@login_required
def delete_object(request, pk):
    # Assuming pk is the primary key of the object you want to delete
    obj = YourModel.objects.get(pk=pk)

    # Check if the user has the permission to delete the object
    if request.user == obj.user:
        obj.delete()
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            response_data = {'msg': 'Object deleted successfully!'}
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        else:
            messages.success(request, 'Object deleted successfully!')
            return redirect('your_redirect_url')  # Replace 'your_redirect_url' with the appropriate URL
    else:
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            response_data = {'msg': 'Permission denied. Unable to delete the object.'}
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=403)
        else:
            messages.error(request, 'Permission denied. Unable to delete the object.')
            return redirect('your_redirect_url')  # Replace 'your_redirect_url' with the appropriate URL
