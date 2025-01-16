from rest_framework import serializers
from .models import Advertisements, Beacons

class BeaconsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacons
        fields = '__all__'

class AdvertisementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisements
        fields = '__all__'

    def validate(self, data):
        """
        Ensure that end_date is greater than start_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date >= end_date:
            raise serializers.ValidationError({"end_date": "End date must be greater than start date." })
        return data

class AdvertisementCountSerializer(serializers.Serializer):
    total_advertisements = serializers.IntegerField()

class TotalBeaconSerializer(serializers.Serializer):
    total_beacons = serializers.IntegerField()

class ActiveBeaconsSerializers(serializers.Serializer):
    active_beacons = serializers.IntegerField()

