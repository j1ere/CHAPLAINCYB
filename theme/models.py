# theme/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Theme(models.Model):
    text = models.TextField(help_text="The main inspirational theme text")
    image = models.ImageField(upload_to='themes/', help_text="Theme banner image")
    year = models.CharField(max_length=50, help_text="e.g., 2024/2025 - Semester 2")
    is_active = models.BooleanField(default=False, help_text="Only one theme should be active at a time")
    date_created = models.DateField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-is_active', '-date_created']
        verbose_name = "Semester Theme"
        verbose_name_plural = "Semester Themes"

    def __str__(self):
        return f"{self.year} - {'Active' if self.is_active else 'Archived'}"

    def save(self, *args, **kwargs):
        # Ensure only one active theme
        if self.is_active:
            Theme.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)