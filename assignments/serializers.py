from rest_framework import serializers
from advertisements.models import Advertisement
from drf_spectacular.utils import extend_schema_field
from beacons.serializers import BeaconSimpleSerializer
from assignments.models import AdvertisementAssignment
from django.utils.timezone import now

class AdvertisementAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementAssignment
        fields = '__all__'

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

class AdvertisementDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementAssignment
        fields = ['end_date']

class AdvertisementWithBeaconsSerializer(serializers.ModelSerializer):
    beacons = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["advertisement_id", "title", "beacons"]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_beacons(self, obj) -> list:
        return [
                {
                    "beacon": BeaconSimpleSerializer(assignment.beacon).data,
                    "start_date": assignment.start_date,
                    "end_date": assignment.end_date
                }
                for assignment in obj.advertisement_assignments.all()
            ]


class AdvertisementAssignmentBeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementAssignment
        fields = ['beacon']