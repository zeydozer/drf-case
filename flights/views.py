from rest_framework import viewsets
from .models import Flight
from .serializers import FlightSerializer
import logging

logger = logging.getLogger(__name__)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Yeni uçuş oluşturuldu: {instance}")
