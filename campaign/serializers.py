from rest_framework import serializers
from .models import Advertisements, Beacons, AdvertisementsLog

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

        if not start_date or not end_date:
            raise serializers.ValidationError({"dates": "Both start_date and end_date must be provided." })
        if start_date >= end_date:
            raise serializers.ValidationError({"end_date": "End date must be greater than start date." })
        return data


class AdvertisementsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementsLog
        fields = '__all__'

