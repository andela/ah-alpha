from django.urls import path

from .views import (ArticleAPIView, SpecificArticle)

app_name = "articles"

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name="articles"),
    path('articles/<str:slug>/', SpecificArticle.as_view(), name="specific_article")
]
