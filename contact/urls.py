# contact/urls.py

from django.urls import path

from .views import (
    AdminMessageListAPIView,
    AdminMarkAsReadAPIView,
    AdminMarkAsRepliedAPIView,
    AdminDeleteMessageAPIView,
    ContactMessageAPIView
)

urlpatterns = [
    # Public
    path("", ContactMessageAPIView.as_view()),

    # Admin
    path("admin/messages/", AdminMessageListAPIView.as_view()),
    path("admin/messages/<int:pk>/read/", AdminMarkAsReadAPIView.as_view()),
    path("admin/messages/<int:pk>/replied/", AdminMarkAsRepliedAPIView.as_view()),
    path("admin/messages/<int:pk>/delete/", AdminDeleteMessageAPIView.as_view()),
]