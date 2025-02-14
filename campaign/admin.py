from django.contrib import admin
from .models import Beacon, Advertisement, AdvertisementLog

# Register your models here.
@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display=('beacon_id', 'location_name', 'signal_strength', 'battery_status', 'start_date', 'status')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=('advertisement_id', 'beacon_id', 'content', 'start_date', 'end_date', 'created_at', 'type')

@admin.register(AdvertisementLog)
class AdvertisementLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'beacon', 'advertisement', 'timestamp')
