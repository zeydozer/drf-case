from rest_framework import viewsets
from .models import Flight
from .serializers import FlightSerializer
from django.core.cache import cache
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Yeni uçuş oluşturuldu: {instance}")
        cache.delete("flight_list_cache")
    
    def list(self, request, *args, **kwargs):
        cache_key = "flight_list_cache"
        data = cache.get(cache_key)

        if data:
            logger.info("✅ Cache'ten alındı.")
            return Response(data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, data, timeout=60)  # 60 saniye cache
        logger.info("📦 DB'den alındı ve cache'e yazıldı.")
        return Response(data)
