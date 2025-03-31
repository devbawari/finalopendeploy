from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser as User
from .serializers import EmployeeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer

from .models import ChatMessage
from .serializers import ChatMessageSerializer

from rest_framework import status
from .models import ChatMessage, ChatHistory
from .serializers import ChatMessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_profile(request):
    user = get_object_or_404(User, id=request.user.id, role="employee")
    serializer = EmployeeSerializer(user)
    return Response({"user": serializer.data})


# Chat history for each employee
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Ensure the user is authenticated
def get_chat_history(request):
    """Returns all chat sessions of the logged-in user"""
    user = request.user  # Assuming authentication is implemented
    chat_sessions = ChatHistory.objects.filter(user=user).order_by('-timestamp')

    response_data = {
        "user_id": user.id,
        "chat_history": [
            {
                "chat_id": chat.id,
                "title": chat.title,
                "timestamp": chat.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            for chat in chat_sessions
        ]
    }
    
    return Response(response_data)


# messages for each chat session
class ChatMessageListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, id):
        try:
            chat_history = ChatHistory.objects.get(id=id)
            messages = ChatMessage.objects.filter(chat=chat_history).order_by('timestamp')
            serializer = ChatMessageSerializer(messages, many=True)

            if chat_history.user != request.user:
                return Response({"error": "You do not have permission to view this chat."},
                                status=status.HTTP_403_FORBIDDEN)

            return Response({
                "user_id": chat_history.user.id,
                "chat_history": serializer.data
            }, status=status.HTTP_200_OK)

        except ChatHistory.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, id):
        """Store both user message & system response in the chat session."""
        chat_history = get_object_or_404(ChatHistory, id=id, user=request.user)

        user_message = request.data.get("message")
        system_response = request.data.get("response")
        mcq_options = request.data.get("mcq", [])
        timestamp = request.data.get("timestamp")

        if not user_message or not system_response:
            return Response({"error": "Both 'message' and 'response' are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Store User's Message (Sent)
        user_chat = ChatMessage.objects.create(
            chat=chat_history,
            user=request.user,
            message=user_message,
            direction="sent",
            timestamp=timestamp
        )

        # Store System's Response (Received)
        system_chat = ChatMessage.objects.create(
            chat=chat_history,
            user=request.user,  # Keeping user association
            message=system_response,
            direction="received",
            timestamp=timestamp
        )

        return Response({
            "chat_id": chat_history.id,
            "messages": [
                {"id": user_chat.id, "message": user_chat.message, "direction": "sent", "timestamp": user_chat.timestamp},
                {"id": system_chat.id, "message": system_chat.message, "direction": "received", "timestamp": system_chat.timestamp}
            ],
            "mcq": mcq_options
        }, status=status.HTTP_201_CREATED)