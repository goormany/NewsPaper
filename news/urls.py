from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path("news/", cache_page(60)(newsListView.as_view()), name='news_list'),
    path("news/<int:pk>", cache_page(60*5)(newsDetailView.as_view()), name='news_detail'),
    path("news/search/", newsSearchView.as_view(), name='news_search'),
    path("news/create/", newsCreateView.as_view(), name='news_create'),
    path("articles/create/", articlesCreateView.as_view(), name='articles_create'),
    path("news/<int:pk>/edit", newsUpdateView.as_view(), name='news_update'),
    path("articles/<int:pk>/edit", articlesUpdateView.as_view(), name='articles_update'),
    path("news/<int:pk>/delete", newsDeleteView.as_view(), name='news_delete'),
    path("articles/<int:pk>/delete", articlesDeleteView.as_view(), name='articles_delete'),
    path("categories/<int:pk>", categoriesView.as_view(), name='categories_list'),
    path('categories/<int:pk>/subscribe', add_me_to_category, name='sub_category'),
    path('categories/', cache_page(60*5)(CategoryListView.as_view()), name='category_lists'),
    path('', IndexView.as_view())
]