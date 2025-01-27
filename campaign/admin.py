from django.contrib import admin
from .models import Beacons, Advertisements

# Register your models here.
@admin.register(Beacons)
class BeaconAdmin(admin.ModelAdmin):
    list_display=('beacon_id', 'location_name', 'signal_strength', 'battery_status', 'start_date', 'status')

@admin.register(Advertisements)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=('advertisement_id', 'beacon_id', 'content', 'start_date', 'end_date', 'created_at', 'type')
