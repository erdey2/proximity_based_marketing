import unittest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class ApiViewTestCase(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_url = reverse('advertisements_list')

        # Set up a valid Bearer token (Replace 'your_actual_token' with a real token)
        self.bearer_token = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4Mjg4MTE4LCJpYXQiOjE3MzgyODc4MTgsImp0aSI6ImMxMGMzOGMxOGFlNjQ3NzU4MTUyYTE1MjNhNzU5Nzg4IiwidXNlcl9pZCI6MX0.kGrfy4OKXEUk7plGGZu3SnUzvo4pklqBZWM3-0J2T80")

    def test_api_get_request(self):
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_request_with_authentication(self):
        # Attach the Bearer token to the request headers
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.bearer_token}')

        response = self.client.get(self.api_url)

        # Check for successful authentication (200 OK or another expected response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Adjust based on expected status code