from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'content', )

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.priority = Task.objects.max_priority() + 1.0
        task.save()
