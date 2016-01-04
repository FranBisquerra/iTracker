from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, TicketForm
from django.shortcuts import redirect
from i_tracker.models import *

# LOGIN VIEW
def login(request):

	login_form = LoginForm(request.POST or None)

	if login_form.is_valid():
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return redirect('home')
			else:
				return HttpResponse("Inactive user.")
		else:
			return redirect('login')

	context = {
		"LoginForm": LoginForm,
	}

	return render(request, "i_tracker/login.html", context)

# LOGOUT VIEW
def logout(request):
	auth_logout(request)
	context = {}
	return redirect('login')

# HOME VIEW
def home(request):

	session = request.session

	uid = session.get('_auth_user_id')

	issues = list(Ticket.objects.filter(user=uid))

	context = {

		"session": session,
		"issues": issues,
	}
	return render(request, "i_tracker/home.html", context)

# TABLE VIEW
def home_table(request):

	context = {

		"session": request.session,
	}
	return render(request, "i_tracker/home_table.html", context)

# ISSUE
def issue(request, issue_pk = None):

	context = {}

	session = request.session

	uid = session.get('_auth_user_id')

	# Check if POST or GET
	if request.method == 'POST':

		# Save
		if issue_pk is None:
			form = TicketForm(request.POST)
			
		# Update
		else:
			instance = Ticket.objects.get(pk=issue_pk)
			form = TicketForm(request.POST, instance=instance)


		# validate form
		if form.is_valid():
			# save data
			form.save()

		# return to the home page with message
		return redirect('home')

	else:

		if issue_pk is not None:
			# get the info.
			issue = Ticket.objects.get(pk=issue_pk)
			ticket_form = TicketForm( initial={ 'name': issue.name,
												'description': issue.description,
												'dateraised': issue.dateraised,
												'datesolved': issue.datesolved,
												'priority': issue.priority,
												'creator': issue.creator,
												'categories': issue.categories.all(),
												'user': issue.user,
												})
		else:
			# set the default info.
			ticket_form = TicketForm( initial={ 'creator': uid })
			issue = None

	context = {

		"TicketForm": ticket_form,
		"issue": issue,
		"session": request.session,
	}

	return render(request, "i_tracker/issue.html", context)