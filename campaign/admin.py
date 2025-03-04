from django.contrib import admin
from .models import Beacon, Advertisement, AdvertisementLog, BeaconMessage

# Register your models here.
@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display=('beacon_id', 'location_name', 'minor', 'major', 'signal_strength', 'battery_status', 'start_date', 'status')

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=('advertisement_id', 'content', 'start_date', 'end_date', 'created_at', 'type')

@admin.register(AdvertisementLog)
class AdvertisementLogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'beacon', 'advertisement', 'timestamp')

@admin.register(BeaconMessage)
class BeaconMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'beacon', 'content', 'type', 'sent_at', 'read_at')