# backend/chatbot/models.py

from django.db import models

class ChatHistory(models.Model):
    user_input = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at}] {self.user_input[:30]}..."
