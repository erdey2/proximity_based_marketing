from django.db import models
from beacons.models import Beacon
from advertisements.models import Advertisement

class AdvertisementLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    beacon = models.ForeignKey(Beacon, on_delete=models.CASCADE, to_field='beacon_id', related_name='logs')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, to_field='advertisement_id', related_name='log')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Delivery: {self.advertisement.title} from {self.beacon.location_name} at {self.timestamp}"
