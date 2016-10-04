from django.db import models


class TaskManager(models.Manager):
    def max_priority(self):
        if self.get_queryset().count() == 0:
            return 0
        else:
            return self.get_queryset().all().aggregate(models.Max('priority'))['priority__max']

    def lift(self, pk):
        pass


# priority를 float 타입으로 설정하는 이유:
# 새로 등록할 경우 -> 기존 맥시멈 + a
# 우선순위를 위아래로 변경할 경우 -> 끼어들어가야 할 자리 위/아래 priority 값의 평균
# 이 방식을 따를 경우 어떤 task의 우선순위를 변경해도, 다른 taks들의 우선순위 값 변동이 없다!
class Task(models.Model):
    BUTTON_UP_TAG = "up"
    BUTTON_DOWN_TAG = "down"

    title = models.CharField(max_length=30)
    content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()

    def __str__(self):
        return self.title

    def button_id_up(self):
        return Task.BUTTON_UP_TAG + '-' + str(self.pk)

    def button_id_down(self):
        return Task.BUTTON_DOWN_TAG + '-' + str(self.pk)
