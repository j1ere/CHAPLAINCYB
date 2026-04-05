# calendar/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from datetime import datetime
from .services.scraper import fetch_readings
from django.core.cache import cache

from .models import CalendarEntry
from .serializers import CalendarEntrySerializer

from django.http import HttpResponse, Http404
from .models import Prayer

from .serializers import PrayerSerializer

import requests

from django.core.cache import cache

from rest_framework import status

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class CalendarEntryViewSet(viewsets.ModelViewSet):
    queryset = CalendarEntry.objects.all()
    serializer_class = CalendarEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'date']
    search_fields = ['event', 'readings', 'verse', 'notes']
    ordering_fields = ['date', 'event']
    ordering = ['date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)  # Optional: keep original creator



class PublicCalendarView(APIView):
    """Public endpoint - Returns all Calendar Entries (no authentication needed)"""
    permission_classes = [AllowAny]

    def get(self, request):
        # Optional: Support query params for filtering
        queryset = CalendarEntry.objects.all().order_by('date')

        # You can add filtering by year if needed later
        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(date__year=year)

        serializer = CalendarEntrySerializer(queryset, many=True)
        
        return Response({
            "count": queryset.count(),
            "calendar_entries": serializer.data
        })
    





from django.core.cache import cache

class DailyReadingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        date_str = request.GET.get("date") or "today"

        cache_key = f"daily_readings_{date_str}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        try:
            if date_str != "today":
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                target_date = None

            data = fetch_readings(target_date)

            cache.set(cache_key, data, timeout=60 * 60 * 12)  # 12 hrs

            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)







# views.py
from django.http import Http404, HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

from .models import Prayer
from .serializers import PrayerSerializer


class PrayerListAPIView(APIView):
    """List all prayers"""
    permission_classes = [AllowAny]

    def get(self, request):
        prayers = Prayer.objects.all().order_by('name')
        serializer = PrayerSerializer(prayers, many=True)
        return Response(serializer.data)


class DownloadPrayerAPIView(APIView):
    """Retrieve a single prayer + support for TXT and PDF download"""
    permission_classes = [AllowAny]

    def get_object(self, prayer_name):
        try:
            return Prayer.objects.get(name__iexact=prayer_name)
        except Prayer.DoesNotExist:
            raise Http404("Prayer not found")

    def generate_pdf(self, prayer):
        """Generate a nicely formatted PDF for the prayer"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawCentredString(width / 2, height - 80, prayer.name.upper())

        # Content
        p.setFont("Helvetica", 12)
        text_object = p.beginText(80, height - 120)
        text_object.setLeading(18)  # Line spacing

        # Split content into lines and wrap properly
        lines = prayer.content.split('\n')
        for line in lines:
            if line.strip() == "":  # Handle blank lines
                text_object.moveCursor(0, 18)
            else:
                text_object.textLine(line.strip())

        p.drawText(text_object)
        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer

    def get(self, request, prayer_name, format=None):
        prayer = self.get_object(prayer_name)

        # PDF Download
        if request.GET.get('download') == 'pdf':
            pdf_buffer = self.generate_pdf(prayer)
            safe_filename = f"{prayer.name.replace(' ', '_').lower()}.pdf"

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
            response.write(pdf_buffer.getvalue())
            return response

        # TXT Download
        if request.GET.get('download') == 'true':
            safe_filename = f"{prayer.name.replace(' ', '_').lower()}.txt"
            response = HttpResponse(prayer.content, content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
            return response

        # Default: Return JSON
        serializer = PrayerSerializer(prayer)
        return Response(serializer.data)




# calendar/views.py

import requests
import html
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DailyVerseView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        cached = cache.get("daily_verse")
        if cached:
            return Response(cached)

        try:
            res = requests.get(
                "https://discoverybiblestudy.org/daily/api/",
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json",
                },
                timeout=10
            )

            res.raise_for_status()
            data = res.json()

            # 🧼 CLEAN DATA
            cleaned = {
                "text": html.unescape(data.get("text", "")).strip(),
                "ref": data.get("ref", "").replace(" :", ":").replace(": ", ": ").strip(),
                "date": data.get("date"),
                "url": data.get("url"),
                "verse_url": data.get("verseUrl"),
            }

            # 💾 Cache cleaned version
            cache.set("daily_verse", cleaned, timeout=12 * 60 * 60)

            return Response(cleaned)

        except requests.exceptions.RequestException as e:
            return Response(
                {
                    "error": "Failed to fetch verse",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )