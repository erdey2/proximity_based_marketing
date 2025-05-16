from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from core.beacons.models import Beacon
from core.advertisements.models import Advertisement
from core.logs.models import AdvertisementLog
from core.beacons.serializers import BeaconSerializer
from uuid import uuid4
from datetime import date
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from django.urls import reverse

class BeaconsModelTest(APITestCase):
    def setUp(self):
        """Setup a test beacon before running tests"""
        self.beacon1 = Beacon.objects.create(
            #beacon_id = uuid4(),
            name="beacon 1",
            location_name="Garment"
        )

    def test_beacon_creation(self):
        #self.assertNotEqual(self.beacon1.beacon_id, None)
        self.assertEqual(self.beacon1.name, "beacon 1")
        self.assertEqual(self.beacon1.location_name, "Garment")
        self.assertEqual(self.beacon1.signal_strength, None)
        self.assertEqual(self.beacon1.battery_status, None)
        self.assertEqual(self.beacon1.minor, None)
        self.assertEqual(self.beacon1.major, None)
        self.assertEqual(self.beacon1.latitude, None)
        self.assertEqual(self.beacon1.longitude, None)
        self.assertEqual(self.beacon1.status, "Inactive")

    def test_is_active(self):
        self.assertEqual(self.beacon1.status, "Inactive")

    def test_change_status(self):
        """Test the change_status() method"""
        self.beacon1.change_status("Inactive")
        self.assertEqual(self.beacon1.status, "Inactive")

    def test_beacon_str_representation(self):
        """Test the __str__ method"""
        self.assertEqual(str(self.beacon1), "beacon 1 Garment (Inactive)")


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

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        # Generate a valid JWT token
        access_token = AccessToken.for_user(self.user)
        self.bearer_token = str(access_token)

        # Set authentication for tests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')

        # create a sample beacon data for testing advertisements
        self.beacon = Beacon.objects.create(name="Beacon 1", location_name="Bole")
        self.advertisement = Advertisement.objects.create(
            advertisement_id = uuid4(),
            beacon_id = self.beacon.pk,
            title="Ybs Soap",
            content="We are offering 30% discount",
            start_date = date(2025, 2, 4),
            end_date = date(2025, 2, 24)
        )

class BeaconView(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.beacons_url = reverse('beacons_list')

    def test_beacons_list(self):
        """Test authenticated access to the beacons list."""
        response = self.client.get(self.beacons_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Authentication failed")

    def test_beacon_create(self):
        # Arrange: Define valid beacon data
        valid_data = {
            "name": "beacon 1",
            "location_name": "Saris",
            "battery_status": 95,
            "signal_strength": 70
        }
        # Act: Send a POST request to create a beacon
        response = self.client.post(self.beacons_url, valid_data, format="json")

        # Assert: Expecting 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["name"], valid_data["name"], response.data)

    def test_beacon_create_invalid_data(self):
        """Test creating a beacon with missing required fields."""

        # Arrange: Define invalid beacon data (missing beacon_name)
        invalid_data = {
            "location_name": "Adey Abeba",
            "battery_status": 95,
            "signal_strength": 70
        }
        # Act: Send a POST request with invalid data
        response = self.client.post(self.beacons_url, invalid_data, format="json")

        # Assert: Expecting 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "required field missed")
        self.assertIn("name", response.data)  # Check that error is related to name

    def test_beacon_create_invalid_signal(self):
        """Test creating a beacon with an invalid signal strength."""

        # Arrange: Define beacon with an invalid signal strength
        invalid_data = {
            "name": "beacon 1",
            "location_name": "Adey Abeba",
            "battery_status": 95,
            "signal_strength": 70
        }
        # Act: Send a POST request with invalid data
        response = self.client.post(self.beacons_url, invalid_data, format="json")

        # Assert: Expecting 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "required field missed")
