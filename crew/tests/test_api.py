from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from flights.models import Flight
from crew.models import CrewMember
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class CrewAPITest(APITestCase):
  def setUp(self):
    """Set up test data"""
    self.admin_user = User.objects.create_user(
      username="admin_crew",
      password="secret123",
      email="admin_crew@test.com",
      role="admin"
    )
    
    self.staff_user = User.objects.create_user(
      username="staff_crew",
      password="secret123",
      email="staff_crew@test.com",
      role="staff"
    )
    
    self.viewer_user = User.objects.create_user(
      username="viewer_crew",
      password="secret123",
      email="viewer_crew@test.com",
      role="viewer"
    )

    # Create test flights
    self.flight1 = Flight.objects.create(
      flight_number="TK2020",
      origin="İstanbul",
      destination="Roma",
      scheduled_time=timezone.now() + timedelta(hours=2),
      status="planned"
    )
    
    self.flight2 = Flight.objects.create(
      flight_number="TK2021",
      origin="Ankara",
      destination="Paris",
      scheduled_time=timezone.now() + timedelta(hours=5),
      status="delayed"
    )

    # Create test crew members
    self.pilot = CrewMember.objects.create(
      name="Ahmet Pilot",
      role="pilot",
      assigned_flight=self.flight1
    )
    
    self.copilot = CrewMember.objects.create(
      name="Ayşe Copilot",
      role="copilot",
      assigned_flight=self.flight1
    )

  def _authenticate_user(self, user):
    """Helper method to authenticate user and set authorization header"""
    token_url = reverse('token_obtain_pair')
    response = self.client.post(token_url, {
      "username": user.username,
      "password": "secret123"
    }, format='json')
    access_token = response.data["access"]
    self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

  def test_crew_create_as_admin(self):
    """Test crew creation by admin user"""
    self._authenticate_user(self.admin_user)
    
    url = reverse('crewmember-list')
    crew_data = {
      "name": "Ali Kaptan",
      "role": "pilot",
      "assigned_flight": self.flight2.id
    }
    response = self.client.post(url, crew_data, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data["role"], "pilot")
    self.assertEqual(response.data["name"], "Ali Kaptan")
    self.assertEqual(response.data["assigned_flight"], self.flight2.id)

  def test_crew_create_as_staff(self):
    """Test crew creation by staff user"""
    self._authenticate_user(self.staff_user)
    
    url = reverse('crewmember-list')
    crew_data = {
      "name": "Fatma Hostes",
      "role": "attendant",
      "assigned_flight": self.flight2.id
    }
    response = self.client.post(url, crew_data, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data["role"], "attendant")

  def test_crew_list_authenticated(self):
    """Test crew list retrieval by authenticated user"""
    self._authenticate_user(self.viewer_user)
    
    url = reverse('crewmember-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertGreaterEqual(len(response.data['results']), 2)  # At least our test crew members

  def test_crew_list_unauthenticated(self):
    """Test crew list access without authentication"""
    url = reverse('crewmember-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 401)

  def test_crew_detail_view(self):
    """Test crew member detail view"""
    self._authenticate_user(self.viewer_user)
    
    url = reverse('crewmember-detail', kwargs={'pk': self.pilot.pk})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["name"], "Ahmet Pilot")
    self.assertEqual(response.data["role"], "pilot")

  def test_crew_update_as_admin(self):
    """Test crew member update by admin"""
    self._authenticate_user(self.admin_user)
    
    url = reverse('crewmember-detail', kwargs={'pk': self.pilot.pk})
    update_data = {
      "name": "Ahmet Senior Pilot",
      "role": "pilot",
      "assigned_flight": self.flight1.id
    }
    response = self.client.put(url, update_data, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["name"], "Ahmet Senior Pilot")

  def test_crew_delete_as_admin(self):
    """Test crew member deletion by admin"""
    self._authenticate_user(self.admin_user)
    
    # Create a crew member to delete
    temp_crew = CrewMember.objects.create(
      name="Temp Crew",
      role="attendant",
      assigned_flight=self.flight1
    )
    
    url = reverse('crewmember-detail', kwargs={'pk': temp_crew.pk})
    response = self.client.delete(url)
    self.assertEqual(response.status_code, 204)
    self.assertFalse(CrewMember.objects.filter(pk=temp_crew.pk).exists())

  def test_crew_filter_by_flight(self):
    """Test filtering crew members by flight"""
    self._authenticate_user(self.viewer_user)
    
    url = reverse('crewmember-list')
    response = self.client.get(url + f"?assigned_flight={self.flight1.id}")
    self.assertEqual(response.status_code, 200)
    
    # Check that all returned crew members are assigned to flight1
    for crew_member in response.data['results']:
      self.assertEqual(crew_member['assigned_flight'], self.flight1.id)

  def test_crew_filter_by_role(self):
    """Test filtering crew members by role"""
    self._authenticate_user(self.viewer_user)
    
    url = reverse('crewmember-list')
    response = self.client.get(url + "?role=pilot")
    self.assertEqual(response.status_code, 200)
    
    # Check that all returned crew members are pilots
    for crew_member in response.data['results']:
      self.assertEqual(crew_member['role'], "pilot")

  def test_crew_role_choices(self):
    """Test crew member role validation"""
    self._authenticate_user(self.admin_user)
    
    url = reverse('crewmember-list')
    invalid_crew_data = {
      "name": "Invalid Role Test",
      "role": "invalid_role",
      "assigned_flight": self.flight1.id
    }
    response = self.client.post(url, invalid_crew_data, format='json')
    self.assertEqual(response.status_code, 400)


class CrewModelTest(APITestCase):
  def setUp(self):
    """Set up test data for model tests"""
    self.flight = Flight.objects.create(
      flight_number="TK3000",
      origin="İzmir",
      destination="Berlin",
      scheduled_time=timezone.now() + timedelta(hours=3),
      status="planned"
    )

  def test_crew_member_str_method(self):
    """Test CrewMember string representation"""
    crew = CrewMember.objects.create(
      name="Test Pilot",
      role="pilot",
      assigned_flight=self.flight
    )
    expected_str = f"Test Pilot (pilot)"
    self.assertEqual(str(crew), expected_str)

  def test_crew_member_creation(self):
    """Test crew member creation with all fields"""
    crew = CrewMember.objects.create(
      name="Test Attendant",
      role="attendant",
      assigned_flight=self.flight
    )
    
    self.assertEqual(crew.name, "Test Attendant")
    self.assertEqual(crew.role, "attendant")
    self.assertEqual(crew.assigned_flight, self.flight)
    self.assertIsNotNone(crew.id)

  def test_crew_member_meta_options(self):
    """Test CrewMember model meta options"""
    self.assertEqual(CrewMember._meta.ordering, ['name'])
    self.assertEqual(CrewMember._meta.verbose_name, 'Crew Member')
    self.assertEqual(CrewMember._meta.verbose_name_plural, 'Crew Members')
