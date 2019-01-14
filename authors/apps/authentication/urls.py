from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

# Define the app name
app_name = "auth"

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="register"),
    path('users/login/', LoginAPIView.as_view(), name="login"),
]
