from rest_framework.test import APITestCase
from django.urls import reverse
from flights.models import Flight
from crew.models import CrewMember

class CrewAPITest(APITestCase):
    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="TK2020",
            origin="İstanbul",
            destination="Roma",
            scheduled_time="2025-08-06T14:00:00Z",
            status="planned"
        )

    def test_crew_create(self):
        url = reverse('crewmember-list')
        crew_data = {
            "name": "Ali Kaptan",
            "role": "pilot",
            "assigned_flight": self.flight.id
        }
        response = self.client.post(url, crew_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["role"], "pilot")

    def test_crew_list(self):
        CrewMember.objects.create(name="Fatma Hostes", role="attendant", assigned_flight=self.flight)
        url = reverse('crewmember-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
