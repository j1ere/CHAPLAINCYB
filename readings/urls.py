# calendar/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CalendarEntryViewSet, PublicCalendarView, DailyReadingsView,
    DownloadPrayerAPIView, DailyVerseView, PrayerViewSet
)
router = DefaultRouter()
router.register(r'entries', CalendarEntryViewSet, basename='calendar-entry')
router.register(r'prayers', PrayerViewSet, basename='prayer')


urlpatterns = [
    path('', include(router.urls)),

    # PUBLIC ENDPOINT - No login required
    path('public/', PublicCalendarView.as_view(), name='public-calendar'),
    path("daily/", DailyReadingsView.as_view(), name="daily-readings"),
    path('prayers/download/<str:prayer_name>/', DownloadPrayerAPIView.as_view(), name='download-prayer'),
    # path('prayers/', PrayerListAPIView.as_view(), name='prayer-list'),
    path("daily-verse/", DailyVerseView.as_view(), name="daily-verse"),


]

