from django import forms

from .models import Label
from .models import Task


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = '__all__'

    def clean_color(self):
        color = self.cleaned_data['color']
        if len(color) != 7:
            raise forms.ValidationError("color 값을 hex code 로 입력해주세요.")
        if color[0] != '#':
            raise forms.ValidationError("color 값을 hex code 로 입력해주세요.")
        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError("color 값을 hex code 로 입력해주세요.")
        return color


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'content', )

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.priority = Task.objects.max_priority() + 1.0
        task.save()
