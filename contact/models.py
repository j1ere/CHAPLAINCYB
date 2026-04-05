# contact/models.py
from django.db import models

class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General Inquiry"),
        ("student", "Student Services"),
        ("events", "Events & Activities"),
        ("groups", "Groups & Movements"),
        ("spiritual", "Spiritual Guidance"),
        ("donations", "Donations & Support"),
        ("partnerships", "Partnerships"),
    ]

    STATUS_CHOICES = [
        ("unread", "Unread"),
        ("read", "Read"),
        ("replied", "Replied"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)

    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="unread")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.category}"