from django.db import models

# Create your models here.
class Task(models.Model):
    taskname=models.CharField(max_length=128)
    deadline=models.DateTimeField()
    priority=models.IntegerField()
    do_repeat=models.BooleanField()
    interval=models.DurationField(blank=True,null=True)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True)