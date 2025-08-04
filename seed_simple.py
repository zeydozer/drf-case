#!/usr/bin/env python
"""
Simple seed script for Django project
Run this from the project root: python seed_simple.py
"""
import os
import sys
import django
from datetime import timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_case.settings')
django.setup()

from django.utils import timezone
from flights.models import Flight
from crew.models import CrewMember


def seed_data():
    print("🚀 Starting to seed data...")

    # Clear existing data
    print("🧹 Clearing existing data...")
    CrewMember.objects.all().delete()
    Flight.objects.all().delete()

    # Sample data
    origins = ['Istanbul', 'Ankara', 'Izmir', 'Antalya', 'Adana', 'Bursa', 'Gaziantep']
    destinations = [
        'London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Amsterdam', 
        'Vienna', 'Barcelona', 'Munich', 'Athens', 'Prague'
    ]
    
    pilot_names = [
        'Ahmet Yılmaz', 'Mehmet Kaya', 'Ali Demir', 'Mustafa Şahin', 
        'Emre Özkan', 'Burak Acar', 'Oğuz Çetin', 'Serkan Bulut'
    ]
    
    copilot_names = [
        'Ayşe Çelik', 'Fatma Arslan', 'Zeynep Kara', 'Elif Güneş', 
        'Seda Aydın', 'Büşra Yıldırım', 'Neslihan Uçar', 'Melis Tan'
    ]
    
    attendant_names = [
        'Burcu Yurt', 'Deniz Tekin', 'Merve Akın', 'Selin Polat', 'Gamze Doğan',
        'Özge Yıldız', 'Pınar Koç', 'Ebru Taş', 'Gizem Öz', 'Tuğba Er',
        'Duygu Arslan', 'Cansu Kaya', 'Beste Çiftçi', 'Nazlı Gün', 'Ece Parlak'
    ]

    statuses = ['planned', 'delayed', 'departed', 'landed']
    
    # Create flights
    print("✈️  Creating flights...")
    flights = []
    for i in range(25):
        flight_number = f"TK{1000 + i}"
        origin = random.choice(origins)
        destination = random.choice(destinations)
        
        # Make sure origin and destination are different
        while destination == origin:
            destination = random.choice(destinations)
        
        # Create scheduled time (random between now and next 45 days)
        base_time = timezone.now()
        random_days = random.randint(0, 45)
        random_hours = random.randint(6, 23)  # Flights between 6 AM - 11 PM
        random_minutes = random.choice([0, 15, 30, 45])
        
        scheduled_time = base_time + timedelta(
            days=random_days, 
            hours=random_hours, 
            minutes=random_minutes
        )
        
        # Weight statuses (more planned flights)
        status_weights = ['planned'] * 50 + ['delayed'] * 20 + ['departed'] * 20 + ['landed'] * 10
        status = random.choice(status_weights)
        
        flight = Flight.objects.create(
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            scheduled_time=scheduled_time,
            status=status
        )
        flights.append(flight)
        
    print(f"✅ Created {len(flights)} flights")

    # Create crew members for each flight
    print("👥 Creating crew members...")
    crew_count = 0
    
    for flight in flights:
        # Each flight needs: 1 pilot, 1 copilot, 2-5 attendants
        
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
        
        # Flight attendants (2-5 per flight)
        num_attendants = random.randint(2, 5)
        selected_attendants = random.sample(attendant_names, min(num_attendants, len(attendant_names)))
        
        for attendant_name in selected_attendants:
            attendant = CrewMember.objects.create(
                name=attendant_name,
                role='attendant',
                assigned_flight=flight
            )
            crew_count += 1

    print(f"✅ Created {crew_count} crew members")
    
    # Display summary
    print("\n🎉 Seed data creation completed!")
    print(f"📊 Summary:")
    print(f"   • Total flights: {Flight.objects.count()}")
    print(f"   • Total crew members: {CrewMember.objects.count()}")
    print(f"   • Planned flights: {Flight.objects.filter(status='planned').count()}")
    print(f"   • Delayed flights: {Flight.objects.filter(status='delayed').count()}")
    print(f"   • Departed flights: {Flight.objects.filter(status='departed').count()}")
    print(f"   • Landed flights: {Flight.objects.filter(status='landed').count()}")
    
    # Display some sample data
    print("\n📋 Sample flights:")
    for flight in Flight.objects.all()[:5]:
        crew_list = ', '.join([f'{c.name} ({c.role})' for c in flight.crew.all()])
        print(f"   {flight.flight_number}: {flight.origin} → {flight.destination}")
        print(f"      Status: {flight.status} | Scheduled: {flight.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"      Crew: {crew_list}")
        print()


if __name__ == '__main__':
    seed_data()
