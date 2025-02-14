from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError

# Create your models here.
def validate_signal_strength(value):
    if value < 0 or value > 100:
        raise ValidationError('Signal strength must be between 0 and 100.')

def validate_battery_status(value):
    if value < 0 or value > 100:
        raise ValidationError('Battery status must be between 0 and 100.')

class Beacon(models.Model):
    beacon_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    signal_strength = models.FloatField(null=True, blank=True, validators=[validate_signal_strength]) # updated by mobile app
    battery_status = models.FloatField(null=True, blank=True, validators=[validate_battery_status]) # updated by mobile app
    start_date = models.DateTimeField(auto_now_add=True)
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        INACTIVE = 'Inactive', 'Inactive'
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INACTIVE)

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
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='advertisement')
    title = models.CharField(max_length=255, null=False, default='ybs soap')
    content = models.TextField(null=False)
    start_date = models.DateTimeField(db_index=True)
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
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} Advertisement ({self.end_date})"

class BeaconMessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='message')
    content = models.CharField(max_length=255)
    class Type(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'
        TEXT = 'text', 'text'
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.TEXT)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.beacon.name} {self.read_at}"


class AdvertisementLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='logs')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, to_field='advertisement_id', related_name='log')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery: {self.advertisement.title} from {self.beacon.location_name} at {self.timestamp}"






