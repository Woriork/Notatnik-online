from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Note(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    #participants
    #user = 
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    #uporządkowanie notatek od najnowszej/ostatnio zmienionej
    class Meta:
        ordering = ['-updated','created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:50]
