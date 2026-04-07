from django.contrib import admin
from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "is_active",
        "date_created",
        "created_by",
    )
    list_filter = ("is_active", "date_created")
    search_fields = ("year", "text")
    readonly_fields = ("date_created", "created_at", "updated_at")

    fieldsets = (
        ("Theme Content", {
            "fields": ("text", "image")
        }),
        ("Academic Period", {
            "fields": ("year",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Meta", {
            "fields": ("created_by", "date_created", "created_at", "updated_at")
        }),
    )

    def save_model(self, request, obj, form, change):
        # Automatically assign the logged-in user if not set
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)