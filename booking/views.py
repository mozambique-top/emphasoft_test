from datetime import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from .filters import RoomFilter
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


@extend_schema_view(
    get=extend_schema(summary='Список комнат', tags=['Комнаты']),
)
class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            # Преобразуйте строки дат в объекты datetime
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Получите список идентификаторов комнат, забронированных в указанный интервал времени
            booked_room_ids = Booking.objects.filter(
                Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
            ).values_list('room_id', flat=True)

            # Фильтрация комнат, исключая те, которые забронированы в указанный интервал времени
            queryset = Room.objects.exclude(id__in=booked_room_ids)
        else:
            queryset = super().get_queryset()

        return queryset


@extend_schema_view(
    put=extend_schema(summary='Детали комнат', tags=['Комнаты']),
    patch=extend_schema(summary="Частичное обновление бронирования", tags=['Комнаты'])
)
class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


@extend_schema_view(
    get=extend_schema(summary="Получение списка бронирований", tags=['Бронирование']),

)
class BookingList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)

    serializer_class = BookingSerializer


@extend_schema_view(
    put=extend_schema(summary="Обновление бронирования", tags=['Бронирование']),
    patch=extend_schema(summary="Частичное обновление бронирования", tags=['Бронирование']),

)
class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@extend_schema_view(
    post=extend_schema(summary='Создание брони', tags=['Бронирования']),
)
class BookingCreate(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Добавляем пользователя к бронированию перед сохранением
        serializer.save(user=self.request.user)


@extend_schema_view(
    delete=extend_schema(summary='Отмена бронирование', tags=['Бронирования']),
    update=extend_schema(summary='Изменить бронирование', tags=['Бронирования'])
)
class BookingCancelAPIView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Проверяем, что текущий пользователь является владельцем бронирования или суперпользователем
        if request.user == instance.user or request.user.is_superuser:
            instance.cancel()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"detail": "You do not have permission to cancel this booking."},
                            status=status.HTTP_403_FORBIDDEN)
