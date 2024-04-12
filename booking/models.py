from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('cancelled', 'Отменено')
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')


