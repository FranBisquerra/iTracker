# -*- encoding: utf-8 -*-
from django.utils.datastructures import MultiValueDict, MergeDict
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from .models import Ticket

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class TicketForm(forms.ModelForm):

	datesolved = forms.DateField(widget=DateTimePicker(options={"format": "DD/MM/YYYY"}), required=False)
	
	class Meta:
		model = Ticket
		fields = '__all__'
