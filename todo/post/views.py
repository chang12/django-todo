from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from .forms import TaskForm
from .models import Task


@staff_member_required()
def index(request):
    return render(request, 'post/index.html', {
        'form': TaskForm(),
        'tasks': Task.objects.all(),
    })
