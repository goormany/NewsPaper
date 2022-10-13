from django.urls import path

from .views import *

urlpatterns = [
    path("", newsListView.as_view()),
    path("<int:pk>", newsDetailView.as_view()),
]
