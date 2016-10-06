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
        'BUTTON_LIFT_TAG': Task.BUTTON_LIFT_TAG,
        'BUTTON_FALL_TAG': Task.BUTTON_FALL_TAG,
    })


@staff_member_required()
def finish(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_active = False
    task.save()
    return redirect(reverse('post:index'))


@staff_member_required()
def modify(request, command):
    fragments = command.split('-')
    if fragments[0] == Task.BUTTON_LIFT_TAG:
        Task.objects.lift(fragments[1])
    elif fragments[0] == Task.BUTTON_FALL_TAG:
        Task.objects.fall(fragments[1])
    return redirect(reverse('post:index'))
