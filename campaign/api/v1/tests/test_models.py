from rest_framework.test import APITestCase
from campaign.models import Beacon, Advertisement, AdvertisementLog
from datetime import timedelta
from django.utils.timezone import now
from uuid import uuid4

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



