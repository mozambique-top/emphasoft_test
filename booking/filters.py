import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    min_capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')

    class Meta:
        model = Room
        fields = ['min_capacity', 'max_price']

