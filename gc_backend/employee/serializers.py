from rest_framework import serializers
from accounts.models import CustomUser as User
from .models import ChatHistory
from .models import ChatMessage

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'post', 'phone', 'department', 'profile_pic', 'role']


# Chat History
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'title', 'timestamp']

# Chat Messages
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'direction', 'message', 'timestamp']
