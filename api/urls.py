from django.urls import path, include
from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from booking.urls import urlpatterns as booking_urls
urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += booking_urls
