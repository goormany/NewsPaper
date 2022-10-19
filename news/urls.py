from django.urls import path

from .views import *

urlpatterns = [
    path("news/", newsListView.as_view(), name='news_list'),
    path("<int:pk>", newsDetailView.as_view(), name='news_detail'),
    path("news/search/", newsSearchView.as_view(), name='news_search'),
    path("news/create/", newsCreateView.as_view(), name='news_create'),
    path("articles/create/", articlesCreateView.as_view(), name='articles_create'),
    path("news/<int:pk>/edit", newsUpdateView.as_view(), name='news_update'),
    path("articles/<int:pk>/edit", articlesUpdateView.as_view(), name='articles_update'),
    path("news/<int:pk>/delete", newsDeleteView.as_view(), name='news_delete'),
    path("articles/<int:pk>/delete", articlesDeleteView.as_view(), name='articles_delete'),
]
