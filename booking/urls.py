from django.urls import path
from .views import RoomList, RoomDetail, BookingList, BookingDetail, BookingCreate, RoomCreate, RoomListSearch, \
    BookingCancelAPIView

urlpatterns = [
    path('rooms/', RoomList.as_view(), name='room-list'),
    path('rooms/search', RoomListSearch.as_view(), name='room-search-with-filter'),
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('rooms/create', RoomCreate.as_view(), name='room-create'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('bookings/create', BookingCreate.as_view(), name='booking-create'),
    path('bookings/cancel/<int:pk>/', BookingCancelAPIView.as_view(), name='booking-cancel')
]