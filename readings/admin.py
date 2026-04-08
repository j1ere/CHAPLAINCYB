# calendar/admin.py
from django.contrib import admin
from .models import CalendarEntry, Prayer
import json


@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'event',
        'type',
        'liturgical_color',
        'created_by',
        'created_at',
    )
    list_filter = ('type', 'liturgical_color', 'date')
    search_fields = ('event', 'notes')
    readonly_fields = ('created_at', 'updated_at')

    # Pretty display of readings
    def formatted_readings(self, obj):
        if not obj.readings:
            return "-"
        try:
            return json.dumps(obj.readings, indent=2)
        except Exception:
            return obj.readings

    formatted_readings.short_description = "Readings"

    # Optional: include in detail view
    fieldsets = (
        (None, {
            'fields': ('date', 'event', 'type', 'liturgical_color')
        }),
        ("Content", {
            'fields': ('readings', 'notes')
        }),
        ("Metadata", {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Prayer)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'content')