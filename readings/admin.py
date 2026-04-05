# calendar/admin.py
from django.contrib import admin
from .models import CalendarEntry, Prayer
import json

@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'event', 'type', 'verse', 'created_by', 'created_at')
    list_filter = ('type', 'date')
    search_fields = ('event', 'verse', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    
    # Optional: Display readings nicely in admin
    def readings_list_display(self, obj):
        return ", ".join(obj.readings) if obj.readings else "-"
    readings_list_display.short_description = "Readings"

@admin.register(Prayer)
class PrayerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'content')