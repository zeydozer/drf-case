from rest_framework import viewsets
from .models import CrewMember
from .serializers import CrewMemberSerializer
from .filters import CrewMemberFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

class CrewMemberPagination(PageNumberPagination):
  """Ekipler için özel sayfalama sınıfı"""
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 100
  page_query_param = 'page'

class CrewMemberViewSet(viewsets.ModelViewSet):
  queryset = CrewMember.objects.all()
  serializer_class = CrewMemberSerializer
  filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
  filterset_class = CrewMemberFilter
  pagination_class = CrewMemberPagination
  search_fields = ('name', 'role')
