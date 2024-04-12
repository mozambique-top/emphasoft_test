import django_filters
from django.db.models import Q

from .models import Room, Booking


class RoomFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='bookings__start_date', method='filter_available_rooms')
    end_date = django_filters.DateFilter(field_name='bookings__end_date', method='filter_available_rooms')
    price_min = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price_per_night", lookup_expr='lte')
    capacity_min = django_filters.NumberFilter(field_name="capacity", lookup_expr='gte')
    capacity_max = django_filters.NumberFilter(field_name="capacity", lookup_expr='lte')
    ordering = django_filters.OrderingFilter(fields=('price_per_night', 'capacity'))

    class Meta:
        model = Room
        fields = ['price_min', 'price_max', 'capacity_min', 'capacity_max', ]

    def filter_available_rooms(self, queryset, name, value):
        if value:
            start_date = self.form.cleaned_data.get('start_date', None)
            end_date = self.form.cleaned_data.get('end_date', None)

            if start_date and end_date:
                booked_rooms = Booking.objects.filter(
                    Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
                ).values_list('room', flat=True)

                queryset = queryset.exclude(id__in=booked_rooms)
            return queryset

        return queryset
