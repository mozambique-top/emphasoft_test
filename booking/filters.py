import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    capacity_min = django_filters.NumberFilter(field_name="capacity", lookup_expr='gte')
    capacity_max = django_filters.NumberFilter(field_name="capacity", lookup_expr='lte')
    ordering = django_filters.OrderingFilter(fields=('price_per_night', 'capacity'))

    class Meta:
        model = Room
        fields = ['price_min', 'price_max', 'capacity_min', 'capacity_max']
