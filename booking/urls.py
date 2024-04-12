from django.urls import path
from .views import RoomListAndCreate, BookingList, BookingUpdateAndCreate, RoomListSearch, \
    BookingCancelAPIView, RoomDetail

urlpatterns = [
    path('rooms/', RoomListAndCreate.as_view(), name='room-list'),
    path('rooms/<int:pk>', RoomDetail.as_view(), name='room-list'),
    path('rooms/search', RoomListSearch.as_view(), name='room-search-with-filter'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingUpdateAndCreate.as_view(), name='booking-update-create'),
    path('bookings/cancel/<int:pk>/', BookingCancelAPIView.as_view(), name='booking-cancel')
]