from django.contrib import admin

from .models import User
from .models import Permission
from .models import Profile
from .models import Priority
from .models import Category
from .models import Ticket
from .models import Comment

# Register your models here.
admin.site.register(Permission)
admin.site.register(Profile)
admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Comment)
