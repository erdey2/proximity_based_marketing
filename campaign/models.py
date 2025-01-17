from django.db import models
import uuid
from django.core.exceptions import ValidationError

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
    title = models.CharField(max_length=255, null=False, default='ybs soap')
    content = models.TextField(null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    media_file = models.FileField(upload_to='advertisements/', null=True, blank=True)

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
        return f"Advertisement {self.title} ({self.type})"




