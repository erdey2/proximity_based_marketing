from django.db import models
from uuid import uuid4

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
