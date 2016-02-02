from .forms import LoginForm, TicketForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages 
from django.core import serializers 
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView # this is the generic view
from i_tracker.models import * 
from i_tracker.tables import TicketTable
import datetime

# LOGIN VIEW
def login(request):
	
	#log out if user logged
	if request.session:
		auth_logout(request)

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
@login_required(login_url='/login/')
def logout(request):
	auth_logout(request)
	context = {}
	return redirect('login')

# HOME VIEW
@login_required(login_url='/login/')
def home(request):

	session = request.session

	uid = session.get('_auth_user_id')

	issues = list(Ticket.objects.filter(user=uid))

	created_issues = list(Ticket.objects.filter(creator=uid))

	if request.user.is_superuser:

		escalated_issues = Ticket.objects.filter(escalated=True)
	else:

		escalated_issues = []
		
	context = {

		"session"          : session,
		"issues"           : issues,
		"created_issues"   : created_issues,
		"escalated_issues" : escalated_issues, 
	}
	return render(request, "i_tracker/home.html", context)

# TABLE VIEW
@login_required(login_url='/login/')
def home_table(request):

	session = request.session

	uid = session.get('_auth_user_id')

	all_issues = list(Ticket.objects.filter(user=uid) | Ticket.objects.filter(creator=uid))

	all_issues_table = TicketTable(all_issues)

	context = {

		"session": request.session,
		"all_issues_table": all_issues_table,
	}
	return render(request, "i_tracker/home_table.html", context)

# ISSUE
@login_required(login_url='/login/')
def issue(request, issue_pk = None):

	context = {}

	session = request.session

	uid = session.get('_auth_user_id')

	recived_msgs = get_messages(request)

	# Check if POST or GET
	if request.method == 'POST':

		# Save
		if issue_pk is None:
			form = TicketForm(request.POST)
			print(request.POST)

			if form.is_valid():
				new_issue = form.save(commit=False)
				new_issue.creator = User.objects.get(id=uid)
				new_issue.dateraised = datetime.datetime.now()

				# save data
				form.save()
				messages.success(request, "La incidencia se ha creado correctamente")
			else:

				messages.error(request, "Ha habido un error inesperado, Compruebe que el formulario es correcto.")
				return redirect(request.META['HTTP_REFERER'])

		# Update
		else:
			instance = Ticket.objects.get(pk=issue_pk)
			form = TicketForm(request.POST, instance=instance)
			
			if form.is_valid():
				updated_issue = form.save(commit=False)
			
				# save data
				form.save()
				messages.success(request, "La incidencia se ha actualizado correctamente")
			else:

				messages.error(request, "Ha habido un error inesperado, Compruebe que el formulario es correcto.")
				return redirect(request.META['HTTP_REFERER'])                             

		# return to the home page with message
		return redirect('home')

	else:

		if issue_pk is not None:
			# get the info.
			issue = Ticket.objects.get(pk=issue_pk)
			ticket_form = TicketForm( initial={ 'name'		  : issue.name,
												'description' : issue.description,
												'dateraised'  : issue.dateraised,
												'datesolved'  : issue.datesolved,
												'priority'    : issue.priority,
												'creator'     : issue.creator,
												'categories'  : issue.categories.all(),
												'user'        : issue.user,
												'escalated'	  : issue.escalated,
												'hidden'	  : issue.hidden,
												'state'		  : issue.state,		
												})
			comments = list(Comment.objects.filter(ticket=issue_pk))

			comment_form = CommentForm()
		else:
			# set the default info.
			ticket_form = TicketForm()
			issue = None
			comments = None
			comment_form = None

		profiles = Profile.objects.all()

	context = {

		"TicketForm" 		 : ticket_form,
		"issue"		 		 : issue,
		"session"	 		 : request.session,
		"comments"	 		 : comments,
		"uid"		 		 : uid,
		"CommentForm"		 : comment_form,
		"messages"	 		 : recived_msgs,
		"profiles"	 		 : profiles,
	}


	return render(request, "i_tracker/issue.html", context)

# ISSUE DELETE
@login_required(login_url='/login/')
def delete_issue(request, issue_pk):

	instance = Ticket.objects.get(pk=issue_pk).delete()
	messages.success(request, 'La incidencia se ha eliminado correctamente.')
	return redirect('home')

# COMMENT
@login_required(login_url='/login/')
def comment(request, issue_pk):

	context = {}

	session = request.session

	uid = session.get('_auth_user_id')

	# Check if POST or GET
	if request.method == 'POST':

		# Save
		form = CommentForm(request.POST)
			
		# validate form
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.user = User.objects.get(id=uid)
			new_comment.ticket = Ticket.objects.get(id=issue_pk)
			# save data
			form.save()
			messages.success(request, 'El mensaje se ha guardado correctamente.')
		else:

			messages.error(request, 'Ha habido un error, intentelo de nuevo en unos minutos.')
			return redirect(request.META['HTTP_REFERER'])

	return redirect('issue', issue_pk=issue_pk)

# COMMENT DELETE
@login_required(login_url='/login/')
def delete_comment(request, comment_pk, issue_pk):

	instance = Comment.objects.get(pk=comment_pk).delete()
	messages.success(request, 'El mensaje se ha eliminado correctamente.')
	return redirect(request.META['HTTP_REFERER'])


# RETURN USERS BY PROFILE
@login_required(login_url='/login/')
def get_users_profile(request):

	profile_pk = request.GET.get('profile_pk')

	if  profile_pk == 0:

		result_set = User.objects.all()
	else:

		results = list(UserProfile.objects.filter(profile=profile_pk))

		result_set = []

		for result in results:

			result_set.append(result.user)

	json_response = serializers.serialize('json', result_set, fields=('username'))

	return HttpResponse(json_response, content_type='application/json')