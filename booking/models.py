from datetime import datetime

from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def is_available(self, start_date_str, end_date_str):

        # Преобразуем строки дат в объекты datetime.date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Получаем список бронирований для этой комнаты
        bookings = self.booking_set.all()

        # Проверяем, что для этой комнаты нет бронирований в указанный период времени
        for booking in bookings:
            if booking.start_date <= end_date and booking.end_date >= start_date:
                return False
        return True
    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('cancelled', 'Отменено')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')


