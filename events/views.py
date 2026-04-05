# events/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import UpcomingEvent, RegularEvent, CalendarFile
from .serializers import (
    UpcomingEventSerializer,
    RegularEventSerializer,
    CalendarFileSerializer,
)


class IsAdminUser(permissions.BasePermission):
    """Only staff/superusers can access these admin endpoints"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class UpcomingEventViewSet(viewsets.ModelViewSet):
    queryset = UpcomingEvent.objects.all()
    serializer_class = UpcomingEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)  # optional: keep original creator


class RegularEventViewSet(viewsets.ModelViewSet):
    queryset = RegularEvent.objects.all()
    serializer_class = RegularEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CalendarFileViewSet(viewsets.ViewSet):
    """Simple ViewSet for uploading/retrieving the two calendar files"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request):
        files = CalendarFile.objects.all()
        serializer = CalendarFileSerializer(files, many=True)
        return Response(serializer.data)

    def create(self, request):
        file_type = request.data.get('file_type')
        file = request.FILES.get('file')

        if not file_type or not file:
            return Response({"error": "file_type and file are required"}, status=status.HTTP_400_BAD_REQUEST)

        if file_type not in ['csa', 'program']:
            return Response({"error": "Invalid file_type"}, status=status.HTTP_400_BAD_REQUEST)

        # Replace existing file of same type
        CalendarFile.objects.filter(file_type=file_type).delete()

        calendar = CalendarFile.objects.create(
            file_type=file_type,
            file=file,
            uploaded_by=request.user
        )

        serializer = CalendarFileSerializer(calendar)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        calendar = get_object_or_404(CalendarFile, pk=pk)
        serializer = CalendarFileSerializer(calendar)
        return Response(serializer.data)
    




# ==================== PUBLIC ENDPOINTS ====================

class PublicUpcomingEventsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        events = UpcomingEvent.objects.all().order_by('date')
        serializer = UpcomingEventSerializer(events, many=True)
        return Response({
            "count": events.count(),
            "upcoming_events": serializer.data
        })


class PublicRegularEventsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        events = RegularEvent.objects.all().order_by('title')
        serializer = RegularEventSerializer(events, many=True)
        return Response({
            "count": events.count(),
            "regular_events": serializer.data
        })


class PublicCalendarFilesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        files = CalendarFile.objects.all()
        serializer = CalendarFileSerializer(files, many=True, context={'request': request})
        return Response({
            "count": files.count(),
            "calendar_files": serializer.data
        })