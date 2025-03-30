from django.urls import path
from .views import employee_profile
from .views import ChatMessageListView
from .views import get_chat_history

urlpatterns = [
    path('profile/', employee_profile, name='employee-profile'),
    path('chat/', get_chat_history, name='employee-chat'),
    path('chat/<int:id>/', ChatMessageListView.as_view(), name='chat-messages'),    ## POST is on existing conversation
]
