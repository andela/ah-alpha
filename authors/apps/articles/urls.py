from django.urls import path

from .views import (ArticleAPIView, SpecificArticle, TagAPIView)

app_name = "articles"

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name="articles"),
    path('articles/<str:slug>/', SpecificArticle.as_view(),
         name="specific_article"),
    path('tags/', TagAPIView.as_view(), name="tags"),
]
