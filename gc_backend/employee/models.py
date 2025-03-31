from django.db import models
from accounts.models import CustomUser as User




class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='employee')
    profile_pic = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.name
    

# chat history 
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    title = models.CharField(max_length=255)  # Title of the chat session
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} - {self.user.username}"
    

# chat messages
class ChatMessage(models.Model):
    chat = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    message = models.TextField()
    direction = models.CharField(max_length=10, choices=[('sent', 'Sent'), ('received', 'Received')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.direction}: {self.message[:20]}"

