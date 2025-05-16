from django.db import models
from core.beacons.models import Beacon
from core.advertisements.models import Advertisement
from django.utils.timezone import now
from uuid import uuid4

class AdvertisementAssignment(models.Model):
    assignment_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='advertisement_assignments')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, to_field='advertisement_id', related_name='advertisement_assignments')
    start_date = models.DateTimeField(db_index=True, default=now)
    end_date = models.DateTimeField(db_index=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('beacon', 'advertisement') # prevents duplicate assignments
        ordering = ['-start_date']
