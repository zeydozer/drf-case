from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from flights.models import Flight
from crew.models import CrewMember
import random


class Command(BaseCommand):
  help = 'Seed the database with sample flight and crew data'

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

    # Clear existing data
    CrewMember.objects.all().delete()
    Flight.objects.all().delete()
    self.stdout.write(self.style.WARNING('Cleared existing data'))

    # Sample data
    origins = ['Istanbul', 'Ankara', 'Izmir', 'Antalya', 'Adana']
    destinations = ['London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Amsterdam', 'Vienna']
    
    pilot_names = [
      'Ahmet Yılmaz', 'Mehmet Kaya', 'Ali Demir', 'Mustafa Şahin', 'Emre Özkan'
    ]
    
    copilot_names = [
      'Ayşe Çelik', 'Fatma Arslan', 'Zeynep Kara', 'Elif Güneş', 'Seda Aydın'
    ]
    
    attendant_names = [
      'Burcu Yurt', 'Deniz Tekin', 'Merve Akın', 'Selin Polat', 'Gamze Doğan',
      'Özge Yıldız', 'Pınar Koç', 'Ebru Taş', 'Gizem Öz', 'Tuğba Er'
    ]

    statuses = ['planned', 'delayed', 'departed', 'landed']

    airlines = [
      'Turkish Airlines', 'Pegasus Airlines', 'SunExpress', 'AnadoluJet', 'AtlasGlobal'
    ]

    gates = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    
    # Create flights
    flights = []
    for i in range(20):
      flight_number = f"TK{1000 + i}"
      origin = random.choice(origins)
      destination = random.choice(destinations)
      
      # Create scheduled time (random between now and next 30 days)
      base_time = timezone.now()
      random_days = random.randint(0, 30)
      random_hours = random.randint(0, 23)
      random_minutes = random.choice([0, 15, 30, 45])
      
      scheduled_time = base_time + timedelta(
        days=random_days, 
        hours=random_hours, 
        minutes=random_minutes
      )
      
      status = random.choice(statuses)
      airline = random.choice(airlines)
      gate = random.choice(gates) if random.choice([True, False]) else None
      
      flight = Flight.objects.create(
        flight_number=flight_number,
        origin=origin,
        destination=destination,
        scheduled_time=scheduled_time,
        status=status,
        airline=airline,
        gate=gate
      )
      flights.append(flight)
    
    self.stdout.write(self.style.SUCCESS(f'Created {len(flights)} flights'))

    # Create crew members for each flight
    crew_count = 0
    for flight in flights:
      # Each flight needs: 1 pilot, 1 copilot, 2-4 attendants
      
      # Pilot
      pilot = CrewMember.objects.create(
        name=random.choice(pilot_names),
        role='pilot',
        assigned_flight=flight
      )
      crew_count += 1
      
      # Co-pilot
      copilot = CrewMember.objects.create(
        name=random.choice(copilot_names),
        role='copilot',
        assigned_flight=flight
      )
      crew_count += 1
      
      # Flight attendants (2-4 per flight)
      num_attendants = random.randint(2, 4)
      selected_attendants = random.sample(attendant_names, num_attendants)
      
      for attendant_name in selected_attendants:
        attendant = CrewMember.objects.create(
          name=attendant_name,
          role='attendant',
          assigned_flight=flight
        )
        crew_count += 1

    self.stdout.write(self.style.SUCCESS(f'Created {crew_count} crew members'))
    
    # Display summary
    self.stdout.write(self.style.SUCCESS('Seed data creation completed!'))
    self.stdout.write(f'Total flights: {Flight.objects.count()}')
    self.stdout.write(f'Total crew members: {CrewMember.objects.count()}')
    
    # Display some sample data
    self.stdout.write(self.style.WARNING('\nSample flights:'))
    for flight in Flight.objects.all()[:5]:
      self.stdout.write(f'  {flight.flight_number}: {flight.origin} → {flight.destination} ({flight.status})')
      crew_list = ', '.join([f'{c.name} ({c.role})' for c in flight.crew.all()])
      self.stdout.write(f'    Crew: {crew_list}')
