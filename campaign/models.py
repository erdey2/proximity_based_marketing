from django.db import models
from uuid import uuid4
from django.utils.timezone import now

class Beacon(models.Model):
    beacon_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    minor = models.IntegerField(null=True, blank=True, default=0)
    major = models.IntegerField(null=True, blank=True, default=0)
    location_name = models.CharField(max_length=100, db_index=True)
    signal_strength = models.FloatField(null=True, blank=True) # updated by mobile app
    battery_status = models.FloatField(null=True, blank=True) # updated by mobile app
    start_date = models.DateTimeField(auto_now_add=True)
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        INACTIVE = 'Inactive', 'Inactive'
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)
    latitude = models.FloatField(null=True, blank=True, default=9.1450)
    longitude = models.FloatField(null=True, blank=True, default=38.7525)

    def __str__(self):
        return f"{self.name} {self.location_name} ({self.status})"

    def is_active(self):
        return self.status == self.Status.ACTIVE

    def change_status(self, new_state):
        if new_state in [self.Status.ACTIVE, self.Status.INACTIVE]:
            self.status = new_state
            self.save()


class Advertisement(models.Model):
    advertisement_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, db_index=True)
    content = models.TextField(null=False)
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
        return f"{self.title} Advertisement ({self.end_date})"


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


class AdvertisementLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='logs')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, to_field='advertisement_id', related_name='log')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Delivery: {self.advertisement.title} from {self.beacon.location_name} at {self.timestamp}"






