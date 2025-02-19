from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from campaign.serializers import BeaconSerializer, AdvertisementSerializer, AdvertisementLogSerializer
from campaign.models import Beacon, Advertisement, AdvertisementLog
from django.utils.timezone import now
from datetime import timedelta
from uuid import uuid4


class SerializerTest(APITestCase):
    def setUp(self):
        self.beacon1 = Beacon.objects.create(name="beacon 1", location_name='Jomo')
        self.advertisement = Advertisement.objects.create(
            beacon=self.beacon1,
            title="Test Ad",
            content="This is a test advertisement.",
            start_date=now(),
            end_date=now() + timedelta(days=10),
            created_at=now(),
            is_active=True,
            type=Advertisement.Type.TEXT,
        )
        self.ad_log = AdvertisementLog.objects.create(
            beacon = self.beacon1,
            advertisement=self.advertisement,
            timestamp=now(),
        )

    def test_serialize_existing_beacon(self):
        """Test serialization of an existing beacon instance"""
        serializer = BeaconSerializer(instance=self.beacon1)

        expected_data = {
            "beacon_id": str(self.beacon1.beacon_id),  # UUID needs to be string
            "name": self.beacon1.name,
            "location_name": self.beacon1.location_name,
            "signal_strength": self.beacon1.signal_strength,
            "battery_status": self.beacon1.battery_status,
            "start_date": self.beacon1.start_date.isoformat().replace("+00:00", "Z"),  # Ensure Zulu format
            "status": self.beacon1.Status.INACTIVE.label,
            "minor": None,
            "major": None,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_valid_beacon_creation_serializer(self):
        """Test if a new beacon can be validated correctly"""
        valid_beacon = {
            "name": "New Beacon",
            "location_name": "Market",
            "signal_strength": 50.0,
            "battery_status": 90.2,
            "start_date": (now() + timedelta(minutes=10)).isoformat(),
            "status": "Active",
        }

        serializer = BeaconSerializer(data=valid_beacon)
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Validation should pass

    def test_invalid_beacon_serializer(self):
        """Test an invalid beacon with missing fields"""
        invalid_beacon = {
            "name": "Invalid Beacon",
            # "location_name" is missing, should trigger validation error
        }
        serializer = BeaconSerializer(data=invalid_beacon)
        self.assertFalse(serializer.is_valid())  # Should fail validation
        self.assertIn("location_name", serializer.errors)  # Check for specific error

    def test_serialize_existing_advertisement(self):
        """Test serialization of an existing advertisement instance"""
        serializer = AdvertisementSerializer(instance=self.advertisement)

        # Convert serializer output to a dict
        serialized_data = dict(serializer.data)

        # Convert beacon_id to a string
        serialized_data["beacon"] = str(serialized_data["beacon"])
        expected_data = {
            "advertisement_id": str(self.advertisement.advertisement_id),  # Convert to string
            "beacon": str(self.advertisement.beacon_id),  # Convert UUID to string
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

    def test_valid_advertisement_serializer(self):
        """Test serializer with valid data"""
        valid_data = {
            "beacon": str(self.beacon1.beacon_id),
            "title": "New Ad",
            "content": "This is a new advertisement.",
            "start_date": (now() + timedelta(minutes=5)).isoformat(),
            "end_date": (now() + timedelta(days=5)).isoformat(),
        }
        serializer = AdvertisementSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_advertisement_serializer(self):
        """Test serializer with missing required fields"""
        invalid_data = {
            "title": "Missing beacon and content",
            "start_date": now().isoformat(),
            "end_date": (now() + timedelta(days=5)).isoformat(),
        }
        serializer = AdvertisementSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("beacon", serializer.errors)  # Expecting beacon_id to be required
        self.assertIn("content", serializer.errors)  # Expecting content to be required

    def test_serialize_existing_advertisement_log(self):
        """Test serialization of an existing advertisement log instance"""
        serializer = AdvertisementLogSerializer(instance=self.ad_log)

        # Convert serialized UUID fields to strings
        serialized_data = dict(serializer.data)
        serialized_data["beacon"] = str(serialized_data["beacon"])
        serialized_data["advertisement"] = str(serialized_data["advertisement"])

        expected_data = {
            "log_id": self.ad_log.log_id,
            "beacon": str(self.ad_log.beacon.beacon_id),  # Convert to string
            "advertisement": str(self.ad_log.advertisement.advertisement_id),  # Convert to string
            "timestamp": self.ad_log.timestamp.isoformat().replace("+00:00", "Z"),  # Ensure correct format
        }
        self.assertEqual(serialized_data, expected_data)





