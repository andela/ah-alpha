from django.urls import path
from django.contrib import admin
# from .views import (createpost, detail_post_view, postpreference)
from . import views
from .models import LikeDislike

app_name = "like"

urlpatterns = [
    path('articles/<slug>/like/', views.PreferenceView.as_view(
        pref='Like'), name='article_like'),
    path('articles/<str:slug>/dislike/', views.PreferenceView.as_view(
        pref='Dislike'), name='article_dislike')
]
