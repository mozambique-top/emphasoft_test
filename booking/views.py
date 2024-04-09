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




@extend_schema_view(
    get=extend_schema(summary='Поиск комнат', tags=['Комнаты']),
)
class RoomListSearch(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter


@extend_schema_view(
    put=extend_schema(summary='Детали комнат', tags=['Комнаты']),
    patch=extend_schema(summary="Частичное обновление бронирования", tags=['Комнаты'])
)
class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


@extend_schema_view(
    post=extend_schema(summary='Создание комнаты', tags=['Комнаты']),
)
class RoomCreate(generics.CreateAPIView):
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
    post=extend_schema(summary='Создание брони', tags=['Бронирование']),
)
class BookingCreate(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        room_id = self.request.data.get('room')
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"detail": "Room does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем доступность комнаты в указанный период времени
        if room.is_available(start_date, end_date):
            serializer.save(user=user, room=room)
            room.is_available = False  # Помечаем комнату как забронированную
            room.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Room is not available for the specified dates."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    delete=extend_schema(summary='Отмена бронирования', tags=['Бронирование']),
)
class BookingCancelAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        booking_id = kwargs.get('pk')
        try:
            instance = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"detail": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if instance.status != 'cancelled':
            instance.status = 'cancelled'
            instance.delete()
            return Response({"detail": "Booking cancelled and deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
