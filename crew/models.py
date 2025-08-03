from django.db import models
from flights.models import Flight

class CrewMember(models.Model):
    ROLE_CHOICES = [
        ('pilot', 'Pilot'),
        ('copilot', 'Co-Pilot'),
        ('attendant', 'Flight Attendant'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='crew')

    def __str__(self):
        return f"{self.name} ({self.role})"
