from rest_framework.test import APITestCase
from django.urls import reverse
from flights.models import Flight
from users.models import User

class FlightAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="secret123")
        self.client.login(username="testuser", password="secret123")

        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {
            "username": "testuser",
            "password": "secret123"
        }, format='json')
        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        self.flight_data = {
            "flight_number": "TK1234",
            "origin": "Ankara",
            "destination": "Berlin",
            "scheduled_time": "2025-08-05T12:00:00Z",
            "status": "planned"
        }
        self.flight = Flight.objects.create(**self.flight_data)

    def test_flight_list(self):
        url = reverse('flight-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_flight_create(self):
        url = reverse('flight-list')
        new_flight = {
            "flight_number": "TK9999",
            "origin": "İzmir",
            "destination": "Madrid",
            "scheduled_time": "2025-08-07T15:00:00Z",
            "status": "delayed"
        }
        response = self.client.post(url, new_flight, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "delayed")

    def test_flight_filter_by_status(self):
        url = reverse('flight-list')
        response = self.client.get(url + "?status=planned")
        self.assertEqual(response.status_code, 200)
        for item in response.data["results"]:
            self.assertEqual(item["status"], "planned")
