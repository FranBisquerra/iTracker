from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
	name 		= models.CharField(max_length=100)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class UserProfile(models.Model):
	user 		= models.ForeignKey(User)
	profile 	= models.ForeignKey(Profile)

class Priority(models.Model):
	name 		= models.CharField(max_length=30)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class State(models.Model):
	name 		= models.CharField(max_length=30)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Category(models.Model):
	name 		= models.CharField(max_length=30)	
	description = models.TextField()

	def __str__(self):              # __unicode__ on Python 2
		return self.name

		
class Ticket(models.Model):
	name 		= models.CharField(max_length=100, blank=False)
	description = models.TextField(blank=False)
	dateraised 	= models.DateField(blank=True, null=True)
	datesolved 	= models.DateField(blank=True, null=True)
	priority 	= models.ForeignKey(Priority, on_delete=models.CASCADE, blank=False)
	creator 	= models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	categories 	= models.ManyToManyField(Category, related_name='ticket_categories', blank=False)
	user 		= models.ForeignKey(User, related_name='ticket_user', on_delete=models.CASCADE, default=0, blank=False)
	state	 	= models.ForeignKey(State, on_delete=models.CASCADE, blank=False)
	escalated 	= models.BooleanField(default=False)
	hidden		= models.BooleanField(default=False)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Comment(models.Model):
	ticket 		= models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=False)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	description = models.TextField(blank=False)