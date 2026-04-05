# theme/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThemeViewSet, PublicActiveThemeView

router = DefaultRouter()
router.register(r'themes', ThemeViewSet, basename='theme')

urlpatterns = [
    path('', include(router.urls)),
    # Optional: direct endpoint to activate a theme
    path('themes/<int:pk>/set-active/', ThemeViewSet.as_view({'post': 'set_active'}), name='theme-set-active'),
    path('public/active-theme/', PublicActiveThemeView.as_view(), name='public-active-theme'),
]