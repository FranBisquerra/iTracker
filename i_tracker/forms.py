# -*- encoding: utf-8 -*-
from django.utils.datastructures import MultiValueDict, MergeDict
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from .models import Ticket, Comment, Priority, Category, User, State

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class TicketForm(forms.ModelForm):

	datesolved 	= forms.DateField(widget=DateTimePicker(options={"format": "DD/MM/YYYY"}), required=False, label='Solucionado')
	name 		= forms.CharField(max_length=100, label='Nombre')
	description = forms.CharField(widget=forms.Textarea(attrs={'rows':7}), label='Descripción')
	priority 	= forms.ModelChoiceField(queryset=Priority.objects.all(), label='Prioridad')
	categories 	= forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Categorias')
	user 		= forms.ModelChoiceField(queryset=User.objects.all(), label='Asignado')
	escalated 	= forms.BooleanField(label='Escalar', initial=False, required=False)
	hidden	 	= forms.BooleanField(label='Archivar', initial=False, required=False)
	state	    = forms.ModelChoiceField(queryset=State.objects.all(), label='Estado', required=True)
	class Meta:
		model  = Ticket
		fields = ['datesolved', 'name', 'description', 'priority', 'categories', 'user', 'escalated', 'hidden', 'state']
		
class CommentForm(forms.ModelForm):
	
	description = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), label='Comentar')

	class Meta:
		model = Comment
		fields = ['description']
