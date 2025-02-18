from rest_framework import serializers
from django.utils.timezone import now
from .models import Advertisement, Beacon, AdvertisementLog, BeaconMessage

class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = '__all__'

class BeaconStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating beacon status"""

    class Meta:
        model = Beacon
        fields = ["status"]  # Only allow updating status
        read_only_fields = ["id"]  # Prevent ID modification

    def validate_status(self, value):
        """Ensure the status is either Active or Inactive"""
        if value not in [Beacon.Status.ACTIVE, Beacon.Status.INACTIVE]:
            raise serializers.ValidationError("Invalid status. Use 'Active' or 'Inactive'.")
        return value

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

    def validate_start_date(self, value):
        """
        Validate that start_date is not in the past.
        """
        current_date = now()
        if value < current_date:
            raise serializers.ValidationError("The start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        """
        Validate that end_date is provided.
        """
        if not value:
            raise serializers.ValidationError("The end date must be provided.")
        return value

    def validate(self, data):
        """
        Ensure that end_date is greater than start_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("The end date must be after the start date.")
        return data


class BeaconMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeaconMessage
        fields = '__all__'


class AdvertisementLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementLog
        fields = '__all__'

