from django.contrib import admin

from .models import Label
from .models import Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Label)
