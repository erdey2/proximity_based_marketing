from django.db import models
from core.beacons.models import Beacon
from uuid import uuid4

class BeaconMessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='message')
    content = models.CharField(max_length=255)
    class Type(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'
        TEXT = 'text', 'text'
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.TEXT)
    sent_at = models.DateTimeField(auto_now_add=True, db_index=True)
    read_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.beacon.name} {self.read_at}"
