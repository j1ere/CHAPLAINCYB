# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UpcomingEventViewSet,
    RegularEventViewSet,
    CalendarFileViewSet,
    PublicUpcomingEventsView,
    PublicRegularEventsView,
    PublicCalendarFilesView,
)

router = DefaultRouter()
router.register(r'upcoming', UpcomingEventViewSet, basename='upcoming')
router.register(r'regular', RegularEventViewSet, basename='regular')

urlpatterns = [
    path('', include(router.urls)),

    # Admin-only endpoints (already existed)
    path('calendars/', CalendarFileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('calendars/<int:pk>/', CalendarFileViewSet.as_view({'get': 'retrieve'})),

    # NEW PUBLIC ENDPOINTS (no login required)
    path('public/upcoming/', PublicUpcomingEventsView.as_view(), name='public-upcoming'),
    path('public/regular/', PublicRegularEventsView.as_view(), name='public-regular'),
    path('public/calendars/', PublicCalendarFilesView.as_view(), name='public-calendars'),
]