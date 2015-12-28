from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from .models import Ticket

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = '__all__'
		widgets = {
			'datesolved': DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
		}