from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CreateUserForm, PasswordChangingForm
from store.models import Customer

# Create your views here.

def user_register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			Customer.objects.create(user=user, name=user.username.upper(), email=user.email)
			return redirect('user_login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.add_message(request, messages.ERROR, "Your credentials are not correct. Please use valid credentials.")
	return render(request, 'accounts/login.html')


def user_logout(request):
	logout(request)
	return redirect('store')


class PasswordChangingView(PasswordChangeView):
	form_class = PasswordChangingForm
	success_url = reverse_lazy('password_change_success')
	template_name = 'accounts/password_change.html'

def password_change_success(request):
	user = request.user
	return render(request, 'accounts/password_change_success.html', {'user':user})


class PasswordResetView(PasswordChangeView):
	form_class = PasswordChangingForm
	success_url = reverse_lazy('password_change_success')
	template_name = 'accounts/password_change.html'