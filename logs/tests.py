from datetime import timedelta
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from beacons.models import Beacon
from advertisements.models import Advertisement
from logs.models import AdvertisementLog
from logs.serializers import AdvertisementLogSerializer
from beacons.tests import BaseAPITestCase
from django.urls import reverse

class AdvertisementLogModelTest(APITestCase):
    """Set up test data"""
    def setUp(self):
        self.beacon1 = Beacon.objects.create(name="beacon 1", location_name="Garment")
        self.ad1 = Advertisement.objects.create(
            title="Test Ad", content="This is a test advertisement.",
            start_date=now(), end_date=now() + timedelta(days=10)
        )
        self.log = AdvertisementLog.objects.create(
            beacon=self.beacon1, advertisement=self.ad1
        )

    def test_log_creation(self):
        """Test log model creation"""
        self.assertEqual(self.log.beacon, self.beacon1)
        self.assertEqual(self.log.advertisement, self.ad1)

    def test_log_str_representation(self):
        """Test the __str__ method"""
        self.assertIn("Delivery:", str(self.log))

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


class AdvertisementLog(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.logs_url = reverse('logs_list')

    def test_logs_list(self):
        response = self.client.get(self.logs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'logs not found')

    def test_valid_log_create(self):
        valid_log = {
            "beacon": self.beacon.pk,
            "advertisement": self.advertisement.pk
        }
        response = self.client.post(self.logs_url, valid_log, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'invalid data')

    def test_invalid_log_create(self):
        invalid_log = {
            "beacon": self.beacon.pk,
        }
        response = self.client.post(self.logs_url, invalid_log, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
