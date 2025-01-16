from django.contrib import admin
from .models import Beacons, Advertisements

# Register your models here.
@admin.register(Beacons)
class BeaconAdmin(admin.ModelAdmin):
    list_display=('uuid', 'location_name', 'signal_strength', 'start_date', 'status')

@admin.register(Advertisements)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=('uuid', 'beacon_id', 'content', 'start_date', 'end_date', 'created_at', 'type')
