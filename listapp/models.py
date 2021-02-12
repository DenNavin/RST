from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
    user = models.ForeignKey(CustomUser, related_name='tags', on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, related_name='tags')
    title = models.CharField(max_length=70)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
