from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# LOGIN VIEW
def login(request):

	print('here')
	login_form = LoginForm(request.POST or None)

	if login_form.is_valid():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('home/')
			else:
				return HttpResponse("Inactive user.")
		else:
			return HttpResponseRedirect('')

	context = {
		"LoginForm": LoginForm,
	}

	return render(request, "i_tracker/login.html", context)

# LOGOUT VIEW
def logout(request):
	auth_logout(request)
	context = {}
	return HttpResponseRedirect('login')

# HOME VIEW
def home(request):
	context = {
		"session": request.session
	}
	return render(request, "i_tracker/home.html", context)

# TABLE VIEW
def home_table(request):
	context = {
		"session": request.session
	}
	return render(request, "i_tracker/home_table.html", context)