from django.urls import path
from .views import CatholicNewsAPIView

urlpatterns = [
    path("", CatholicNewsAPIView.as_view(), name="catholic-news"),
]