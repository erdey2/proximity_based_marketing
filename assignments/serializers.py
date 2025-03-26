from rest_framework import serializers
from beacons.models import Beacon
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from drf_spectacular.utils import extend_schema_field
from beacons.serializers import BeaconSimpleSerializer
from assignments.models import AdvertisementAssignment
from django.utils.timezone import now
from typing import List
from drf_spectacular.utils import extend_schema_field

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

class AdvertisementAssignmentBeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementAssignment
        fields = ['beacon']

class BeaconAdvertisementsSerializer(serializers.ModelSerializer):
    advertisements = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField(allow_empty=True)))
    def get_advertisements(self, obj):  # Adjust the return type if necessary
        return AdvertisementSerializer(
            [assignment.advertisement for assignment in obj.advertisement_assignments.all()], many=True
        ).data

    class Meta:
        model = Beacon
        fields = ['beacon_id', 'name', 'location_name', 'advertisements']

class AdvertisementBeaconAssignmentSerializer(serializers.Serializer):
    beacon = BeaconSimpleSerializer()
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    end_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)

class AdvertisementBeaconsSerializer(serializers.ModelSerializer):
    beacons = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["advertisement_id", "title", "beacons"]

    @extend_schema_field(AdvertisementBeaconAssignmentSerializer(many=True))
    def get_beacons(self, obj) -> list:
        return [
            {
                "beacon": BeaconSimpleSerializer(assignment.beacon).data,
                "start_date": assignment.start_date.isoformat() if assignment.start_date else None,
                "end_date": assignment.end_date.isoformat() if assignment.end_date else None,
            }
            for assignment in obj.advertisement_assignments.all()
        ]
