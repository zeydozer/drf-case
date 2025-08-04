from django.test import TestCase
from flights.models import Flight
from unittest.mock import patch

class FlightSignalTest(TestCase):
    def setUp(self):
        self.flight = Flight.objects.create(
            flight_number="TK8888",
            origin="İzmir",
            destination="Berlin",
            scheduled_time="2025-08-07T11:00:00Z",
            status="planned"
        )

    @patch("notifications.tasks.send_flight_delay_notification.delay")
    def test_status_delayed_triggers_notification(self, mock_task):
        self.flight.status = "delayed"
        self.flight.save()
        self.assertTrue(mock_task.called)
        mock_task.assert_called_with(self.flight.pk, self.flight.flight_number)
