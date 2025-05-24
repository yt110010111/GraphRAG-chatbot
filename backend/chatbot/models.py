from django.db import models
from django.utils import timezone

class ChatHistory(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat {self.id}: {self.user_input[:50]}..."