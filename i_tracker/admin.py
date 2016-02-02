from django.contrib import admin

from .models import User
from .models import UserProfile
from .models import Profile
from .models import Priority
from .models import Category
from .models import Ticket
from .models import Comment
from .models import State

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Priority)
admin.site.register(State)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Comment)
