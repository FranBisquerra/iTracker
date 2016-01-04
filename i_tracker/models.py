from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Permission(models.Model):
	name 		= models.CharField(max_length=30)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Profile(models.Model):
	name 		= models.CharField(max_length=100)
	description = models.TextField()
	idpermision = models.ForeignKey(Permission, on_delete=models.CASCADE)
	users 		= models.ManyToManyField(User)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Priority(models.Model):
	name 		= models.CharField(max_length=30)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Category(models.Model):
	name 		= models.CharField(max_length=30)	
	description = models.TextField()

	def __str__(self):              # __unicode__ on Python 2
		return self.name

		
class Ticket(models.Model):
	name 		= models.CharField(max_length=100)
	description = models.TextField()
	dateraised 	= models.DateField(default=timezone.now)
	datesolved 	= models.DateField(blank=True, null=True)
	priority 	= models.ForeignKey(Priority, on_delete=models.CASCADE)
	creator 	= models.ForeignKey(User, on_delete=models.CASCADE)
	categories 	= models.ManyToManyField(Category, related_name='ticket_categories')
	user 		= models.ForeignKey(User, related_name='ticket_user', on_delete=models.CASCADE, default=0)

	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Comment(models.Model):
	ticket 		= models.ForeignKey(Ticket, on_delete=models.CASCADE)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()