from django.urls import path
from .views import MessageList, MessageDetail

urlpatterns = [
    path('', MessageList.as_view(), name='message_list'),
    path('<uuid:pk>/', MessageDetail.as_view(), name='message_details')
]
