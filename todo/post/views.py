from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from .models import Task


class TaskView(CreateView):
    model = Task
    fields = ('title', 'content')

    success_url = '/'

    @method_decorator(staff_member_required())
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)
