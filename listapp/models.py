from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=70, blank=False)
    description = models.TextField(max_length=800)
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.title, self.date)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Tag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
