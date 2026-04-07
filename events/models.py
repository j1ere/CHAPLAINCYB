# events/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CalendarFile(models.Model):
    """Single model for both Chaplaincy Calendar and Program Guide PDFs"""
    TYPE_CHOICES = (
        ('csa', 'Chaplaincy Calendar'),
        ('program', 'Program Guide'),
    )

    
    file_type = models.CharField(max_length=10, choices=TYPE_CHOICES, unique=True)
    # file = models.FileField(upload_to='calendars/')

    file_url = models.URLField(null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.file_url}"
    
    class Meta:
        verbose_name = "Calendar File"
        verbose_name_plural = "Calendar Files"


class UpcomingEvent(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=100)  # e.g., "10:00 AM"
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # Charity, Recreation, etc.
    icon = models.CharField(max_length=100, blank=True, default="Calendar")  # e.g., "Heart"
    color = models.CharField(max_length=100, blank=True, default="from-blue-500 to-indigo-600")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"


class RegularEvent(models.Model):
    title = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)  # e.g., "Every Sunday"
    time = models.CharField(max_length=100)      # e.g., "8:00 AM & 6:00 PM"
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # Mass & Liturgy, Spiritual, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title