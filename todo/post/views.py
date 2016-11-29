from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .forms import LabelForm
from .forms import TaskForm
from .models import Label
from .models import Task


@staff_member_required()
def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            response_dict = {'success': False}
            for key, value in form.errors.items():
                # field 하나에 여러개의 에러가 있다면 첫번째 것만 반환
                response_dict[key] = value[0]
            return JsonResponse(response_dict)

    elif request.method == 'GET':
        return render(request, 'post/index.html', {
            'tasks': Task.objects.filter(status=Task.DOING),
            'BUTTON_LIFT_TAG': Task.BUTTON_LIFT_TAG,
            'BUTTON_FALL_TAG': Task.BUTTON_FALL_TAG,
            'labels': Label.objects.all(),
        })


@staff_member_required()
def backlog(request):
    return render(request, 'post/backlog.html', {
        'tasks': Task.objects.filter(status=Task.BACKLOG)
    })


@staff_member_required()
def finish(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = Task.DONE
    task.updated_at = datetime.now()
    task.save()
    return redirect(reverse('post:index'))


@staff_member_required()
def move(request, command):
    fragments = command.split('-')
    if fragments[0] == Task.BUTTON_LIFT_TAG:
        Task.objects.lift(fragments[1])
    elif fragments[0] == Task.BUTTON_FALL_TAG:
        Task.objects.fall(fragments[1])
    return JsonResponse({}, status=200)


@staff_member_required()
def modify(request, pk):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        task = get_object_or_404(Task, pk=pk)
        task.title = title
        task.content = content
        task.save()
    return redirect(reverse('post:index'))


@staff_member_required()
def hold_off(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = Task.BACKLOG
    task.updated_at = datetime.now()
    task.save()
    return redirect(reverse('post:index'))


@staff_member_required()
def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    original_status = task.status
    task.status = Task.DELETED
    task.updated_at = datetime.now()
    task.save()
    if original_status is Task.DOING:
        return redirect(reverse('post:index'))
    else:
        return redirect(reverse('post:backlog'))


@staff_member_required()
def start(request, pk):
    task = get_object_or_404(Task, pk=pk, status=Task.BACKLOG)
    task.start()
    return redirect(reverse('post:backlog'))


@staff_member_required()
def label_create(request):
    form = LabelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    else:
        response_dict = {'success': False}
        for key, value in form.errors.items():
            # field 하나에 여러개의 에러가 있다면 첫번째 것만 반환
            response_dict[key] = value[0]
        return JsonResponse(response_dict)


@staff_member_required()
def label_modify(request, pk):
    if request.method == 'POST':
        label = Label.objects.get(pk=pk)
        name = request.POST.get('name', label.name)
        color = request.POST.get('color', label.color)
        label.name = name
        label.color = color
        label.save()
    return JsonResponse({'success': True})


@staff_member_required()
def label_delete(request):
    label_id = request.POST.get('label_id')
    label = Label.objects.get(id=label_id)
    label.delete()
    return JsonResponse({'success': True})


@staff_member_required()
def labeling(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        label_ids = request.POST.getlist('label_ids[]')

        task = Task.objects.get(id=task_id)
        task.labels.set(label_ids)
        task.save()

        return JsonResponse({'success': True})
    else:
        task_id = request.GET.get('task_id')
        task = Task.objects.get(id=task_id)
        label_ids = list(task.labels.values_list('id', flat=True))
        return JsonResponse({'label_ids': label_ids})
