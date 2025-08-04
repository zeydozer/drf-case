import django_filters
from .models import CrewMember


class CrewMemberFilter(django_filters.FilterSet):
    """CrewMember model için filtreleme sınıfı"""

    # İsim ve rol için kısmi eşleşme
    name = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.MultipleChoiceFilter(
        choices=CrewMember.ROLE_CHOICES,
        lookup_expr='in'
    )

    class Meta:
        model = CrewMember
        fields = {
            'name': ['exact', 'icontains'],
            'role': ['exact', 'in'],
        }
