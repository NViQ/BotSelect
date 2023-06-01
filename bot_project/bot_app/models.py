from django.db import models

class Conversation(models.Model):
    user_id = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    response = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)