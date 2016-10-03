from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .forms import TaskForm
from .models import Task


@staff_member_required()
def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('post:index'))
    form = TaskForm()
    return render(request, 'post/index.html', {
        'form': form,
        'tasks': Task.objects.filter(is_active=True).order_by('-priority'),
    })


@staff_member_required()
def erase(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect(reverse('post:index'))
