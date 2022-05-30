from django.db import models

# Create your models here.

class TaskResult(models.Model):
    id = models.UUIDField(
        "ID",
        primary_key=True
    )
    name = models.CharField(
        "任务名称",
        blank=False, 
        max_length=60
    )
    ctime = models.DateTimeField(
        "创建日期",
        auto_now_add=True
    )
    class Meta:
        ordering = ["-ctime", ]