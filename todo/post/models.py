from statistics import mean

from django.db import models


class TaskManager(models.Manager):
    def max_priority(self):
        if self.get_queryset().count() == 0:
            return 0
        else:
            return self.get_queryset().all().aggregate(models.Max('priority'))['priority__max']

    def lift(self, pk):
        sorted_tasks = self.get_queryset().filter(status=Task.DOING).order_by('-priority')
        for idx, task in enumerate(sorted_tasks):
            if task.pk == int(pk):
                break
        if idx == 0:
            return
        elif idx == 1:
            task.priority = sorted_tasks[0].priority + 1.0
        else:
            task.priority = mean([sorted_tasks[idx-2].priority, sorted_tasks[idx-1].priority])
        task.save()

    def fall(self, pk):
        sorted_tasks = self.get_queryset().filter(status=Task.DOING).order_by('priority')
        for idx, task in enumerate(sorted_tasks):
            if task.pk == int(pk):
                break
        if idx == 0:
            return
        elif idx == 1:
            task.priority = sorted_tasks[0].priority - 1.0
        else:
            task.priority = mean([sorted_tasks[idx-2].priority, sorted_tasks[idx-1].priority])
        task.save()


# priority를 float 타입으로 설정하는 이유:
# 새로 등록할 경우 -> 기존 맥시멈 + a
# 우선순위를 위아래로 변경할 경우 -> 끼어들어가야 할 자리 위/아래 priority 값의 평균
# 이 방식을 따를 경우 어떤 task의 우선순위를 변경해도, 다른 taks들의 우선순위 값 변동이 없다!
class Task(models.Model):
    BUTTON_LIFT_TAG, BUTTON_FALL_TAG = "lift", "fall"
    DELETED, BACKLOG, DOING, DONE = -1, 0, 1, 2

    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    status = models.SmallIntegerField(default=DOING)
    priority = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    objects = TaskManager()

    class Meta:
        ordering = ['-priority', ]

    def __str__(self):
        return self.title

    def lift_button_id(self):
        return Task.BUTTON_UP_TAG + '-' + str(self.pk)

    def fall_button_id(self):
        return Task.BUTTON_DOWN_TAG + '-' + str(self.pk)

    def start(self):
        self.status = Task.DOING
        self.priority = Task.objects.max_priority() + 1
        self.save()


class Label(models.Model):
    name = models.CharField(max_length=15)
    color = models.CharField(max_length=7, default="#bfdadc")

    def font_color(self):
        # 예를 들어 #123456 -> 12, 34, 56 으로 split 하고 -> 18, 52, 86 으로 int 값 변환
        red, green, blue = int(self.color[1:3], 16), int(self.color[3:5], 16), int(self.color[5:7], 16)
        # http://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
            return "#000000"
        else:
            return "#280800"
