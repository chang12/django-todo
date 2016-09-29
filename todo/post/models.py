from django.db import models


# priority를 float 타입으로 설정하는 이유:
# 새로 등록할 경우 -> 기존 맥시멈 + a
# 우선순위를 위아래로 변경할 경우 -> 끼어들어가야 할 자리 위/아래 priority 값의 평균
# 이 방식을 따를 경우 어떤 task의 우선순위를 변경해도, 다른 taks들의 우선순위 값 변동이 없다!
class Task(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if Task.objects.count() == 0:
            self.priority = 0
        else:
            self.priority = Task.objects.all().aggregate(models.Max('priority'))['priority__max']
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
