from django.urls import path
from .views import RoomList, RoomDetail, BookingList, BookingDetail, BookingCreate

urlpatterns = [
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('bookings/create', BookingCreate.as_view(), name='booking-create')
]