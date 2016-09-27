from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .forms import TaskForm


@staff_member_required()
def index(request):
    return render(request, "post/index.html", {
        'form': TaskForm,
    })

