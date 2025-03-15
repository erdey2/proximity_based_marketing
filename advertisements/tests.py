from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from beacons.models import Beacon
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse
from beacons.tests import BaseAPITestCase

class AdvertisementModelTest(APITestCase):
    def setUp(self):
        """Setup test data"""
        self.beacon1 = Beacon.objects.create(name="beacon 1", location_name="Garment")
        self.ad1 = Advertisement.objects.create(
            title="Test Ad", content="This is a test advertisement.",
            start_date = now(), end_date = now() + timedelta(days=10)
        )

    def test_advertisement_creation(self):
        """Test if Advertisement is created correctly"""
        self.assertEqual(self.ad1.title, "Test Ad")
        self.assertEqual(self.ad1.content, "This is a test advertisement.")
        self.assertEqual(self.ad1.type, Advertisement.Type.TEXT)

    def test_advertisement_str_representation(self):
        """Test the __str__ method"""
        self.assertIn("Test Ad Advertisement", str(self.ad1))


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

class AdvertisementView(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.advertisements_url = reverse('advertisements_list')

    def test_advertisements_list(self):
        response = self.client.get(self.advertisements_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_advertisement(self):
        valid_data = {
            "beacon": self.beacon.pk,
            "title": "ybs asbeza",
            "content": "We are offering 30% offer visit us",
            "start_date": (now() + timedelta(days=1)),
            "end_date": now() + timedelta(days=10)
        }
        response = self.client.post(self.advertisements_url, valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_advertisement_invalid_data(self):
        invalid_date = {
            "beacon_id": self.beacon.pk,
            "title":  "Ybs asbeza",
            "content": "We are offering 30% offer visit us",
            "start_date": "2025-02-04",
            "end_date": "2025-02-04"
        }
        response = self.client.post(self.advertisements_url, invalid_date, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

