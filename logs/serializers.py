from rest_framework import serializers
from logs.models import AdvertisementLog

class AdvertisementLogSerializer(serializers.ModelSerializer):
    beacon_name = serializers.CharField(source="advertisement.beacon.name", read_only=True)
    advertisement_title = serializers.CharField(source="advertisement.title", read_only=True)
    advertisement_content = serializers.CharField(source="advertisement.content", read_only=True)

    class Meta:
        model = AdvertisementLog
        fields = ['beacon_id', 'beacon_name', 'log_id', 'timestamp', 'advertisement_title', 'advertisement_content', 'beacon_name']

class AdvertisementLogPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementLog
        fields = ['advertisement']