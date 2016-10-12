from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .forms import TaskForm
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
