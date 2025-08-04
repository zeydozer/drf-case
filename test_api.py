#!/usr/bin/env python
import os
import django
from django.conf import settings

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_case.settings')
django.setup()

from django.test import Client
from flights.models import Flight

def test_flight_api():
  client = Client()
  
  # Mevcut veriler
  print("=" * 50)
  print("MEVCUT FLIGHT VERİLERİ")
  print("=" * 50)
  flights = Flight.objects.all()[:5]
  for f in flights:
    print(f"{f.flight_number}: {f.origin} -> {f.destination} ({f.status})")
  
  print(f"\nToplam uçuş sayısı: {Flight.objects.count()}")
  
  # Test 1: Temel API
  print("\n" + "=" * 50)
  print("TEST 1: TEMEL API")
  print("=" * 50)
  response = client.get('/api/flights/')
  print(f"Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    if isinstance(data, list):
      print(f"Cache'den gelen liste uzunluğu: {len(data)}")
    else:
      print(f"Toplam: {data.get('count')}")
      print(f"Bu sayfa: {len(data.get('results', []))}")
  
  # Test 2: Origin filtreleme
  print("\n" + "=" * 50)
  print("TEST 2: ORIGIN FİLTRELEME")
  print("=" * 50)
  
  # Antalya'dan kalkan uçuşlar
  response = client.get('/api/flights/?origin=Antalya')
  print(f"Origin=Antalya Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    results = data.get('results', data if isinstance(data, list) else [])
    print(f"Antalya'dan kalkan uçuş sayısı: {len(results)}")
    for flight in results:
      print(f"  {flight['flight_number']}: {flight['origin']} -> {flight['destination']}")
  
  # Ankara'dan kalkan uçuşlar
  response = client.get('/api/flights/?origin=Ankara')
  print(f"\nOrigin=Ankara Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    results = data.get('results', data if isinstance(data, list) else [])
    print(f"Ankara'dan kalkan uçuş sayısı: {len(results)}")
    for flight in results:
      print(f"  {flight['flight_number']}: {flight['origin']} -> {flight['destination']}")
  
  # Test 3: Kısmi arama (icontains)
  print("\n" + "=" * 50)
  print("TEST 3: KISMI ARAMA")
  print("=" * 50)
  response = client.get('/api/flights/?origin=anta')
  print(f"Origin=anta (kısmi) Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    results = data.get('results', data if isinstance(data, list) else [])
    print(f"'anta' içeren origin sayısı: {len(results)}")
    for flight in results:
      print(f"  {flight['flight_number']}: {flight['origin']} -> {flight['destination']}")
  
  # Test 4: Status filtreleme
  print("\n" + "=" * 50)
  print("TEST 4: STATUS FİLTRELEME")
  print("=" * 50)
  response = client.get('/api/flights/?status=departed')
  print(f"Status=departed Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    results = data.get('results', data if isinstance(data, list) else [])
    print(f"Departed durumundaki uçuş sayısı: {len(results)}")
  
  # Test 5: Sayfalama
  print("\n" + "=" * 50)
  print("TEST 5: SAYFALAMA")
  print("=" * 50)
  response = client.get('/api/flights/?page=1&page_size=5')
  print(f"Page=1&page_size=5 Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    print(f"Sayfa 1, 5 kayıt: {len(data.get('results', []))}")
  
  # Test 6: Arama
  print("\n" + "=" * 50)
  print("TEST 6: ARAMA")
  print("=" * 50)
  response = client.get('/api/flights/?search=TK')
  print(f"Search=TK Status: {response.status_code}")
  if response.status_code == 200:
    data = response.json()
    results = data.get('results', data if isinstance(data, list) else [])
    print(f"'TK' içeren uçuş sayısı: {len(results)}")
  
  print("\n" + "=" * 50)
  print("TEST TAMAMLANDI")
  print("=" * 50)

if __name__ == '__main__':
  test_flight_api()
