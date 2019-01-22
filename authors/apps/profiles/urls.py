from django.urls import path

from .views import (UserProfileView, AuthorsProfileListAPIView,
                    UpdateUserProfileView)


app_name = "prof"

urlpatterns = [
    path('profiles/', AuthorsProfileListAPIView.as_view(),
         name='authors_profile'),
    path('profiles/<str:username>/', UserProfileView.as_view(),
         name='profile'),
    path('profiles/<str:username>/edit/',
         UpdateUserProfileView.as_view(), name='update_profile')
]
