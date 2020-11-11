from django.db import models
from django.contrib.auth.models import User

import datetime

class ChatSession(models.Model):
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.users.__str__()

    class Meta:
        verbose_name = 'ChatSession'
        verbose_name_plural = 'ChatSessions'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(ChatSession, on_delete=models.DO_NOTHING)

    content = models.TextField('Content', blank=True, null=True)
    time = models.DateTimeField('Time')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'