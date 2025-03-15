from celery import shared_task
from .models import Advertisement
from django.utils.timezone import now

@shared_task
def deactivate_expired_ads():
    """Set advertisements as inactive if their end_date has passed."""
    expired_ads = Advertisement.objects.filter(end_date__lt=now(), is_active=True)
    expired_ads.update(is_active=False)
    return f"Updated {expired_ads.count()} expired advertisements."