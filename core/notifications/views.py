from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from drf_spectacular.views import extend_schema
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

class NotificationListView(generics.ListAPIView):
    """ Retrieve a list of notifications for the authenticated user, ordered by the most recent. """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @extend_schema(
        summary="List User Notifications",
        description="Returns a list of notifications belonging to the authenticated user, sorted by creation date descending.",
        responses={200: NotificationSerializer(many=True)},
        tags=["Notifications"]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@login_required
def unread_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = [
        {
            "message": n.message,
            "timestamp": n.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for n in notifications
    ]
    return JsonResponse(data, safe=False)
