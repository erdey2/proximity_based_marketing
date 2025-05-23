from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Advertisement
from django.contrib.auth import get_user_model
from core.notifications.models import Notification

User = get_user_model()

@receiver(post_save, sender=Advertisement)
def create_ad_notification(sender, instance, created, **kwargs):
    if created:
        # Notify all users except the creator
        users = User.objects.exclude(id=instance.createt_by.id)
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"New advertisement posted: {instance.title}"
            )
