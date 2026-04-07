# events/admin.py
from django.contrib import admin
from .models import CalendarFile, UpcomingEvent, RegularEvent
from django.utils.html import format_html

@admin.register(CalendarFile)
class CalendarFileAdmin(admin.ModelAdmin):
    list_display = ('file_type', 'file_link', 'uploaded_at', 'uploaded_by')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('file_url',)
    readonly_fields = ('uploaded_at',)

    def file_link(self, obj):
        if obj.file_url:
            return format_html(
                '<a href="{}" target="_blank">View File</a>',
                obj.file_url
            )
        return "-"
    
    file_link.short_description = "File"

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'category', 'created_by', 'created_at')
    list_filter = ('date', 'category')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(RegularEvent)
class RegularEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'schedule', 'time', 'location', 'category', 'created_by', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at')