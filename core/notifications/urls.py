from django.urls import path
from .views import NotificationListView, unread_notifications

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread/', unread_notifications, name='unread_notifications'),
]
