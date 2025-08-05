from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Flight
from .serializers import FlightSerializer
from .filters import FlightFilter
from django.core.cache import cache
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


class FlightPagination(PageNumberPagination):
  """Uçuşlar için özel sayfalama sınıfı"""
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 100
  page_query_param = 'page'


class FlightViewSet(viewsets.ModelViewSet):
  queryset = Flight.objects.all()
  serializer_class = FlightSerializer
  pagination_class = FlightPagination
  filterset_class = FlightFilter
  permission_classes = [IsAuthenticated]
  
  # Filtreleme ve sıralama backend'leri
  filter_backends = [
    DjangoFilterBackend,
    OrderingFilter,
    SearchFilter
  ]
  
  # Sıralanabilir alanlar
  ordering_fields = [
    'scheduled_time', 
    'flight_number', 
    'origin', 
    'destination', 
    'status'
  ]
  ordering = ['-scheduled_time']  # Varsayılan sıralama (en yeni tarih önce)
  
  # Arama yapılabilir alanlar
  search_fields = [
    'flight_number', 
    'origin', 
    'destination'
  ]

  def get_permissions(self):
    """Define permissions based on action and user role"""
    if self.action in ['create', 'update', 'partial_update', 'destroy']:
      # Only allow authenticated users (role-based filtering can be added later)
      permission_classes = [IsAuthenticated]
    else:
      # All authenticated users can view flight data
      permission_classes = [IsAuthenticated]
    
    return [permission() for permission in permission_classes]

  def perform_create(self, serializer):
    instance = serializer.save()
    logger.info(f"Yeni uçuş oluşturuldu: {instance}")
    # Tüm cache'leri temizle çünkü yeni veri eklenmiş
    cache.clear()
  
  def perform_update(self, serializer):
    instance = serializer.save()
    logger.info(f"Uçuş güncellendi: {instance}")
    # Tüm cache'leri temizle çünkü veri değişmiş
    cache.clear()
  
  def perform_destroy(self, instance):
    logger.info(f"Uçuş silindi: {instance}")
    instance.delete()
    # Tüm cache'leri temizle çünkü veri silinmiş
    cache.clear()
  
  def list(self, request, *args, **kwargs):
    # Sadece filtresiz ve arama parametresi olmayan istekleri cache'le
    has_filters = bool(request.query_params.get('flight_number') or 
                      request.query_params.get('origin') or 
                      request.query_params.get('destination') or
                      request.query_params.get('status') or
                      request.query_params.get('scheduled_time_after') or
                      request.query_params.get('scheduled_time_before') or
                      request.query_params.get('scheduled_date') or
                      request.query_params.get('search') or
                      request.query_params.get('ordering'))
    
    has_pagination = bool(request.query_params.get('page') or 
                         request.query_params.get('page_size'))
    
    # Eğer herhangi bir filtre, arama veya sayfalama parametresi varsa cache kullanma
    if has_filters or has_pagination:
      logger.info("🔍 Filtreleme/sayfalama var, doğrudan DB'den çekiliyor")
      return super().list(request, *args, **kwargs)
    
    # Cache logic sadece tüm veriler için
    cache_key = "flight_list_cache_all"
    data = cache.get(cache_key)

    if data:
      logger.info("✅ Cache'ten alındı.")
      return Response(data)

    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    data = serializer.data
    cache.set(cache_key, data, timeout=300)  # 5 dakika cache
    logger.info("📦 DB'den alındı ve cache'e yazıldı.")
    return Response(data)
