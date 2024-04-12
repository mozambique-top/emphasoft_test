from django.urls import path
from .views import RoomList, BookingList, BookingUpdateAndCreate, RoomListSearch, \
    BookingCancelAPIView

urlpatterns = [
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/search', RoomListSearch.as_view(), name='room-search-with-filter'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingUpdateAndCreate.as_view(), name='booking-update-create'),
    path('bookings/cancel/<int:pk>/', BookingCancelAPIView.as_view(), name='booking-cancel')
]