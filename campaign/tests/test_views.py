from rest_framework.test import APITestCase
from rest_framework import status
from campaign.models import Advertisements, Beacons, AdvertisementsLog
from datetime import datetime, timedelta
import uuid

class TestAdvertisement(APITestCase):
    def setUp(self):
        # Create a test beacon
        self.beacon = Beacons.objects.create(uuid=uuid.uuid4(), location_name="Bole", signal_strength=10, battery_status=78)
        self.advertisement = Advertisements.objects.create(beacon_id='', content='', start_date='', end_date='')

        # Create test advertisements
        self.advertisement1 = Advertisements.objects.create(
            beacon_id=self.beacon, title="Ad 1", content="Description for Ad 1", start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=7), is_active=True, type="text"
        )
        self.advertisement2 = Advertisements.objects.create(
            beacon_id=self.beacon,
            title="Ad 2",
            content="Description for Ad 2",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=14),
            is_active=True,
            type="image"
        )


    def test_advertisements_list(self):
        # Use the APIClient to send a GET request to the advertisements endpoint
        response = self.client.get('/api/advertisements/')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'incorrect end point')
        self.assertEqual(len(response.data), 2)  # Ensure 2 advertisements are returned

        # Validate the structure of the first advertisement
        first_ad = response.data[0]
        self.assertIn('uuid', first_ad)
        self.assertIn('beacon_id', first_ad)
        self.assertIn('title', first_ad)
        self.assertIn('content', first_ad)
        self.assertIn('start_date', first_ad)
        self.assertIn('end_date', first_ad)
        self.assertIn('is_active', first_ad)
        self.assertIn('type', first_ad)