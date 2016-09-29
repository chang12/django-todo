from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .forms import TaskForm
from .models import Task


@staff_member_required()
def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    form = TaskForm()
    return render(request, 'post/index.html', {
        'form': form,
        'tasks': Task.objects.all().order_by('-priority'),
    })
