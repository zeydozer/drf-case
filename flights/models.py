from django.db import models

class Flight(models.Model):
  STATUS_CHOICES = [
    ('planned', 'Planned'),
    ('delayed', 'Delayed'),
    ('departed', 'Departed'),
    ('landed', 'Landed'),
  ]

  flight_number = models.CharField(max_length=10, unique=True)
  origin = models.CharField(max_length=100)
  destination = models.CharField(max_length=100)
  scheduled_time = models.DateTimeField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')

  def __str__(self):
    return f"{self.flight_number} - {self.origin} → {self.destination}"
