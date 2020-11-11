from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    
    content = models.TextField('Content', blank=True, null=True)
    time = models.DateTimeField('Time')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class ChatSession(models.Model):
    users = models.ManyToManyField(User)
    messages = models.ManyToManyField(Message)

    class Meta:
        verbose_name = 'Собеседник'
        verbose_name_plural = 'Собеседники'
