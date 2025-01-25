from django.db import models
import uuid

# Create your models here.
class Beacons(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    location_name = models.CharField(max_length=100)
    signal_strength = models.FloatField()
    battery_status = models.FloatField(default=100)
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
    beacon_id = models.ForeignKey(Beacons, on_delete=models.CASCADE, to_field='uuid', db_column='beacon_id')
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

class AdvertisementsLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    beacon = models.ForeignKey(Beacons, on_delete=models.CASCADE, to_field='uuid')
    advertisement = models.ForeignKey(Advertisements, on_delete=models.CASCADE, to_field='uuid')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery: {self.advertisement.title} from {self.beacon.location_name} at {self.timestamp}"





