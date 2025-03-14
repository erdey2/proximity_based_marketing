from django.contrib import admin
from .models import Beacon, Advertisement, AdvertisementLog, BeaconMessage, AdvertisementAssignment

# Register your models here.
admin.site.register(Beacon)
admin.site.register(Advertisement)
admin.site.register(BeaconMessage)
admin.site.register(AdvertisementLog)
admin.site.register(AdvertisementAssignment)
