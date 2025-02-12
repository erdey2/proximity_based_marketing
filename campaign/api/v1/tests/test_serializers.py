from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from campaign.serializers import BeaconsSerializer, AdvertisementsSerializer, AdvertisementsLogsSerializer
from campaign.models import Beacons, Advertisements, AdvertisementsLog
from django.utils.timezone import now
from datetime import timedelta


class SerializerTest(APITestCase):
    def setUp(self):
        self.beacon1 = Beacons.objects.create(name="beacon 1", location_name='Jomo')
        self.advertisement = Advertisements.objects.create(
            beacon_id=self.beacon1,
            title="Test Ad",
            content="This is a test advertisement.",
            start_date=now(),
            end_date=now() + timedelta(days=10),
            created_at=now(),
            is_active=True,
            type=Advertisements.Type.TEXT,
        )

    def test_serialize_existing_beacon(self):
        """Test serialization of an existing beacon instance"""
        serializer = BeaconsSerializer(instance=self.beacon1)

        expected_data = {
            "beacon_id": str(self.beacon1.beacon_id),  # UUID needs to be string
            "name": self.beacon1.name,
            "location_name": self.beacon1.location_name,
            "signal_strength": self.beacon1.signal_strength,
            "battery_status": self.beacon1.battery_status,
            "start_date": self.beacon1.start_date.isoformat().replace("+00:00", "Z"),  # Ensure Zulu format
            "status": self.beacon1.Status.INACTIVE.label
        }

        self.assertEqual(serializer.data, expected_data)

    def test_valid_beacon_creation_serializer(self):
        """Test if a new beacon can be validated correctly"""
        valid_beacon = {
            "beacon_id": str(self.beacon1.beacon_id),  # UUID
            "name": "New Beacon",
            "location_name": "Market",
            "signal_strength": 80.5,
            "battery_status": 90.2,
            "start_date": self.beacon1.start_date.isoformat(),  # Convert DateTime to string
            "status": "Active",
        }

        serializer = BeaconsSerializer(data=valid_beacon)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Validation should pass

    def test_invalid_beacon_serializer(self):
        """Test an invalid beacon with missing fields"""
        invalid_beacon = {
            "name": "Invalid Beacon",
            # "location_name" is missing, should trigger validation error
        }
        serializer = BeaconsSerializer(data=invalid_beacon)
        self.assertFalse(serializer.is_valid())  # Should fail validation
        self.assertIn("location_name", serializer.errors)  # Check for specific error

    def test_serialize_existing_ad(self):
        """Test serialization of an existing advertisement instance"""
        serializer = AdvertisementsSerializer(instance=self.advertisement)

        # Convert serializer output to a dict
        serialized_data = dict(serializer.data)

        # Convert beacon_id to a string
        serialized_data["beacon_id"] = str(serialized_data["beacon_id"])


        expected_data = {
            "advertisement_id": str(self.advertisement.advertisement_id),  # Convert to string
            "beacon_id": str(self.advertisement.beacon_id.beacon_id),  # Convert UUID to string
            "title": self.advertisement.title,
            "content": self.advertisement.content,
            "start_date": self.advertisement.start_date.isoformat().replace("+00:00", "Z"),
            "end_date": self.advertisement.end_date.isoformat().replace("+00:00", "Z"),
            "created_at": self.advertisement.created_at.isoformat().replace("+00:00", "Z"),
            "is_active": self.advertisement.is_active,
            "media_file": None,
            "type": self.advertisement.get_type_display(),  # Ensure 'type' is properly formatted
        }
        self.assertEqual(serialized_data, expected_data)


