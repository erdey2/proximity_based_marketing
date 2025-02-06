from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from campaign.models import Beacons, Advertisements
from datetime import date
from uuid import uuid4

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
        self.beacon = Beacons.objects.create(name="Beacon 1", location_name="Bole")
        self.advertisement = Advertisements.objects.create(
            advertisement_id = uuid4(),
            beacon_id = self.beacon,
            title="Ybs Soap",
            content="We are offering 30% discount",
            start_date = date(2025, 2, 4),
            end_date = date(2025, 2, 24)
        )

class BeaconsView(BaseAPITestCase):
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
            "signal_strength": -70
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
            "signal_strength": -70
        }
        # Act: Send a POST request with invalid data
        response = self.client.post(self.beacons_url, invalid_data, format="json")

        # Assert: Expecting 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "required field missed")
        self.assertIn("name", response.data)  # Check that error is related to name


class AdvertisementsView(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.advertisements_url = reverse('advertisements_list')

    def test_advertisements_list(self):
        response = self.client.get(self.advertisements_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_advertisement(self):
        valid_data = {
            "beacon_id": self.beacon.pk,
            "title": "ybs asbeza",
            "content": "We are offering 30% offer visit us",
            "start_date": "2025-02-04",
            "end_date": "2025-03-05"
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

class AdvertisementsLogs(BaseAPITestCase):
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

