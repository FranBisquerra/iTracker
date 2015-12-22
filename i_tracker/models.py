from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Permission(models.Model):
	name 		= models.CharField(max_length=30)

class Profile(models.Model):
	name 		= models.CharField(max_length=100)
	description = models.TextField()
	idpermision = models.ForeignKey(Permission, on_delete=models.CASCADE)
	users 		= models.ManyToManyField(User)

class Priority(models.Model):
	name 		= models.CharField(max_length=30)

class Category(models.Model):
	name 		= models.CharField(max_length=30)	
	description = models.TextField()
		
class Ticket(models.Model):
	name 		= models.CharField(max_length=100)
	description = models.TextField()
	dateraised 	= models.DateTimeField(default=timezone.now)
	datesolved 	= models.DateTimeField(blank=True, null=True)
	priority 	= models.ForeignKey(Priority, on_delete=models.CASCADE)
	creator 	= models.ForeignKey(User, on_delete=models.CASCADE)
	categories 	= models.ManyToManyField(Category, related_name='ticket_categories')
	users 		= models.ManyToManyField(User,  related_name='ticket_users')

class Comment(models.Model):
	ticket 	= models.ForeignKey(Ticket, on_delete=models.CASCADE)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()