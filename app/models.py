from django.db import models


class Priority(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT)
    event_id = models.CharField(max_length=30)

    class Meta:
        ordering = ['-priority', 'created']
