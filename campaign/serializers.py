from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.utils.timezone import now
from .models import Advertisement, Beacon, AdvertisementLog, BeaconMessage, AdvertisementAssignment

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['advertisement_id', 'title', 'content', 'start_date', 'end_date', 'is_active']

    def validate_start_date(self, value):
        """ Validate that start_date is not in the past. """
        current_date = now()
        if value < current_date:
            raise serializers.ValidationError("The start date cannot be in the past.")
        return value

    def validate_end_date(self, value):
        """ Validate that end_date is provided. """
        if not value:
            raise serializers.ValidationError("The end date must be provided.")
        return value

    def validate(self, data):
        """ Ensure that end_date is greater than start_date. """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("The end date must be after the start date.")
        return data

class BeaconListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['beacon_id', 'minor', 'major', 'signal_strength', 'battery_status', 'latitude', 'longitude']

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

class BeaconSerializer(serializers.ModelSerializer):
    advertisements = serializers.SerializerMethodField()

    def get_advertisements(self, obj):
        """Retrieve the list of advertisement IDs linked to this beacon."""
        return [assignment.advertisement.id for assignment in AdvertisementAssignment.objects.filter(beacon=obj)]

    """ def get_advertisements(self, obj):
        return AdvertisementSerializer(
            [assignment.advertisement for assignment in obj.advertisement_assignments.all()], many=True).data """

    class Meta:
        model = Beacon
        fields = ['beacon_id', 'name', 'location_name', 'advertisements']

class BeaconSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['beacon_id', 'name', 'location_name']

class BeaconPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beacon
        fields = ['beacon_id', 'minor', 'major', 'signal_strength', 'battery_status', 'latitude', 'longitude']

class AdvertisementWithBeaconsSerializer(serializers.ModelSerializer):
    beacons = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["advertisement_id", "title", "start_date", 'end_date', "beacons"]

    """ @extend_schema_field(serializers.ListField(child=serializers.UUIDField()))
    def get_beacons(self, obj) -> list:
        return BeaconSimpleSerializer(
            [assignment.beacon for assignment in obj.advertisement_assignments.all()], many=True).data """

    @extend_schema_field(serializers.ListField(child=serializers.UUIDField()))  # Correct return type
    def get_beacons(self, obj):
        return [assignment.beacon.id for assignment in obj.advertisement_assignments.all()]  # Return list of UUIDs

class AdvertisementAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementAssignment
        fields = ['beacon', 'advertisement', 'assigned_at']

class BeaconStatusSerializer(serializers.ModelSerializer):
    """ Serializer for updating beacon status"""
    class Meta:
        model = Beacon
        fields = ["status"]  # Only allow updating status
        read_only_fields = ["id"]  # Prevent ID modification

    def validate_status(self, value):
        """ Ensure the status is either Active or Inactive"""
        if value not in [Beacon.Status.ACTIVE, Beacon.Status.INACTIVE]:
            raise serializers.ValidationError("Invalid status. Use 'Active' or 'Inactive'.")
        return value

class BeaconMessageSerializer(serializers.ModelSerializer):
    beacon_name = serializers.CharField(source="beacon.name", read_only=True)

    class Meta:
        model = BeaconMessage
        fields = ['message_id', 'content', 'sent_at', 'read_at', 'beacon_id', 'beacon_name']

class AdvertisementLogSerializer(serializers.ModelSerializer):
    beacon_name = serializers.CharField(source="advertisement.beacon.name", read_only=True)
    advertisement_title = serializers.CharField(source="advertisement.title", read_only=True)

    class Meta:
        model = AdvertisementLog
        fields = ['beacon_id', 'log_id', 'timestamp', 'advertisement_title', 'beacon_name']

