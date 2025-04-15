from django.db import models
from common.models import CustomUser

class ChatRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_requests')
    engineer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='engineer_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"ChatRequest(user={self.user.username}, engineer={self.engineer.username})"
    

class Message(models.Model):
    chat_request = models.ForeignKey(ChatRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message(sender={self.sender.username}, message={self.message[:20]})"