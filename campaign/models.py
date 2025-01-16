from django.db import models
from django.db.models import Count
from django.utils.timezone import now
import uuid

# Create your models here.
class Beacons(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    location_name = models.CharField(max_length=100)
    signal_strength = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        INACTIVE = 'Inactive', 'Inactive'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.INACTIVE
    )

    def __str__(self):
        return f"{self.location_name} ({self.status})"


class Advertisements(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    beacon_id = models.ForeignKey(Beacons, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Type(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'
        TEXT = 'text', 'text'

    type = models.CharField(
        max_length = 10,
        choices=Type.choices,
        default = Type.TEXT
    )

    def __str__(self):
        return f"Advertisement {self.uuid} ({self.type})"




