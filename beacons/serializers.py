from rest_framework import serializers
from .models import Beacon

class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = '__all__'

    def validate_minor(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError('value must be a numeric')
        return value

    def validate_major(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError('value must be numeric')
        return value

    def validate_signal_strength(self, value):
        """ Ensure signal strength is between -100 and 0."""
        if value is not None and ( value < -100 or value > 0 ):
            raise serializers.ValidationError('Signal strength must be between -100 and 0.')
        return value

    def validate_battery_status(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('battery status must be between 0 and 100')
        return value

class BeaconSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['name', 'location_name']

class BeaconDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['beacon_id', 'minor', 'major', 'signal_strength', 'battery_status', 'latitude', 'longitude']

class BeaconLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['beacon_id', 'name', 'latitude', 'longitude']

class BeaconStatusSerializer(serializers.ModelSerializer):
    """ Serializer for updating beacon status"""
    class Meta:
        model = Beacon
        fields = ['status']  # Only allow updating status
        read_only_fields = ["beacon_id"]  # Prevent ID modification

    def validate_status(self, value):
        """ Ensure the status is either Active or Inactive"""
        if value not in [Beacon.Status.ACTIVE, Beacon.Status.INACTIVE]:
            raise serializers.ValidationError("Invalid status. Use 'Active' or 'Inactive'.")
        return value


