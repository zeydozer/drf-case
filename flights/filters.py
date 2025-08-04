import django_filters
from .models import Flight


class FlightFilter(django_filters.FilterSet):
  """Flight model için filtreleme sınıfı"""
  
  # Uçuş numarası için partial matching
  flight_number = django_filters.CharFilter(lookup_expr='icontains')
  
  # Kalkış ve varış noktaları için partial matching
  origin = django_filters.CharFilter(lookup_expr='icontains')
  destination = django_filters.CharFilter(lookup_expr='icontains')
  
  # Tarih aralığı filtreleri
  scheduled_time_after = django_filters.DateTimeFilter(
    field_name='scheduled_time', 
    lookup_expr='gte',
    label='Scheduled after'
  )
  scheduled_time_before = django_filters.DateTimeFilter(
    field_name='scheduled_time', 
    lookup_expr='lte',
    label='Scheduled before'
  )
  
  # Durum filtresi (çoklu seçim için)
  status = django_filters.MultipleChoiceFilter(
    choices=Flight.STATUS_CHOICES,
    lookup_expr='in'
  )
  
  # Tarih filtresi (sadece gün bazında)
  scheduled_date = django_filters.DateFilter(
    field_name='scheduled_time__date',
    label='Scheduled date'
  )

  class Meta:
    model = Flight
    fields = {
      'flight_number': ['exact', 'icontains'],
      'origin': ['exact', 'icontains'],
      'destination': ['exact', 'icontains'],
      'status': ['exact', 'in'],
      'scheduled_time': ['exact', 'gte', 'lte', 'range'],
    }
