# calendar/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CalendarEntry(models.Model):
    TYPE_CHOICES = [
        ('solemnity', 'Solemnity'),
        ('feast', 'Feast'),
        ('memorial', 'Memorial'),
        ('season', 'Season'),
        ('optional', 'Optional Memorial'),
    ]

    COLOR_CHOICES = [
        ('white', 'White'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('violet', 'Violet / Purple'),
    ]

    date = models.DateField()
    event = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='feast')
    readings = models.JSONField(default=list)  # Store list of readings as JSON
    # verse = models.CharField(max_length=100, blank=True, null=True)
    liturgical_color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        blank=True,
        null=True,
        default=None
    )
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = "Calendar Entry"
        verbose_name_plural = "Calendar Entries"

    def __str__(self):
        return f"{self.date} - {self.event}"

    @property
    def readings_list(self):
        return self.readings
    


class Prayer(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="e.g., 'Our Father'")
    content = models.TextField(help_text="The actual text of the prayer")

    class Meta:
        ordering = ['name']
        verbose_name = "Prayer"
        verbose_name_plural = "Prayers"

    def __str__(self):
        return self.name