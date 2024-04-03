from .views import RegistrationView, ChangePasswordView
from django.urls import path, include
urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name='reg'),
    path('users/change-passwd', ChangePasswordView.as_view(), name='change_passwd'),

]