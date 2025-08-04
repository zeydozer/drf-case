#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_case.settings')
django.setup()

from flights.models import Flight

print("STATUS VERİLERİ:")
print("=" * 40)

# Tüm status'ları say
status_counts = {}
for flight in Flight.objects.all():
    status = flight.status
    status_counts[status] = status_counts.get(status, 0) + 1

for status, count in status_counts.items():
    print(f"{status}: {count} uçuş")

print("\nÖRNEK STATUS'LAR:")
print("=" * 40)
for flight in Flight.objects.all()[:10]:
    print(f"{flight.flight_number}: {flight.status}")
