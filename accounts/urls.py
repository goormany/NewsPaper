from django.urls import path

from .views import *

urlpatterns = [
    path("account/update/<int:pk>", accountUserUpdateView.as_view(), name='account_update'),
]
