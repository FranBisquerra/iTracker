from django.views.generic.edit import DeleteView # this is the generic view
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, TicketForm, CommentForm
from django.shortcuts import redirect
from i_tracker.models import * 
from i_tracker.tables import TicketTable

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

	context = {

		"session": session,
		"issues": issues,
		"created_issues": created_issues,
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
			ticket_form = TicketForm( initial={ 'name'		  : issue.name,
												'description' : issue.description,
												'dateraised'  : issue.dateraised,
												'datesolved'  : issue.datesolved,
												'priority'    : issue.priority,
												'creator'     : issue.creator,
												'categories'  : issue.categories.all(),
												'user'        : issue.user,
												})
			comments = list(Comment.objects.filter(ticket=issue_pk))
		else:
			# set the default info.
			ticket_form = TicketForm( initial={ 'creator': uid })
			issue = None
			comments = None
	

	context = {

		"TicketForm": ticket_form,
		"issue"		: issue,
		"session"	: request.session,
		"comments"	: comments,
		"uid"		: uid,
	}

	return render(request, "i_tracker/issue.html", context)

# ISSUE DELETE
@login_required(login_url='/login/')
def delete_issue(request, issue_pk):

	instance = Ticket.objects.get(pk=issue_pk).delete()
	return redirect('home')

# COMMENT
@login_required(login_url='/login/')
def comment(request, issue_pk, comment_pk=None):

	context = {}

	session = request.session

	uid = session.get('_auth_user_id')

	# Check if POST or GET
	if request.method == 'POST':

		# Save
		if comment_pk is None:
			form = CommentForm(request.POST)
			
		# Update
		else:
			instance = Comment.objects.get(pk=comment_pk)
			form = CommentForm(request.POST, instance=instance)


		# validate form
		if form.is_valid():
			# save data
			form.save()

			comment_pk = None

	if comment_pk is not None:

		# get the info.
		comment = Comment.objects.get(pk=comment_pk)
		comment_form = CommentForm( initial={'ticket'    : issue_pk,
											'user'       : uid,
											'description': comment.description})

	else:
		# set the default info.
		comment_form = CommentForm( initial={'ticket': issue_pk,
											'user'   : uid })
		comment = None	

	older_comments = list(Comment.objects.filter(ticket=issue_pk))	

	context = {

		"CommentForm"   : comment_form,
		"comment"       : comment,
		"session"       : request.session,
		"older_comments": older_comments,
		"issue_pk"      : issue_pk,
		"uid"           : uid,
	}

	return render(request, "i_tracker/comment.html", context)

# COMMENT DELETE
@login_required(login_url='/login/')
def delete_comment(request, comment_pk, issue_pk):

	if request.method == 'POST':

		instance = Comment.objects.get(pk=comment_pk).delete()

		return redirect(request.META['HTTP_REFERER'])
	else:

		context = {

			'comment_pk': comment_pk,
		}

		return render(request, "i_tracker/delete_comment.html", context)