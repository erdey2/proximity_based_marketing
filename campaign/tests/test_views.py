from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

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

class BeaconsView(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.beacons_url = reverse('beacons_list')

    def test_beacons_list_get(self):
        """Test unauthenticated access to the beacons list."""
        response = self.client.get(self.beacons_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_beacons_list_get_with_authentication(self):
        """Test authenticated access to the beacons list."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')
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
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')

        # Act: Send a POST request to create a beacon
        response = self.client.post(self.beacons_url, valid_data, format="json")

        # Assert: Expecting 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["name"], valid_data["name"], response.data)

    def test_create_beacon_invalid_data(self):
        """Test creating a beacon with missing required fields."""

        # Arrange: Define invalid beacon data (missing beacon_id)
        invalid_data = {
            "location_name": "Adey Abeba",
            "battery_status": 95,
            "signal_strength": -70
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')
        # Act: Send a POST request with invalid data
        response = self.client.post(self.beacons_url, invalid_data, format="json")

        # Assert: Expecting 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "required field missed")
        self.assertIn("name", response.data)  # Check that error is related to name


class AdvertisementsView(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.advertisements_url = reverse('advertisements_list')

    def test_advertisements_list(self):
        response = self.client.get(self.advertisements_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'authorization failed')

    def test_advertisements_list_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')



