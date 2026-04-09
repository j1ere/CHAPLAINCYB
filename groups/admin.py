from django.contrib import admin
from .models import Group, GroupImage


class GroupImageInline(admin.TabularInline):
    model = GroupImage
    extra = 1
    fields = ("image", "order", "uploaded_at", "preview")
    readonly_fields = ("uploaded_at", "preview")
    ordering = ("order", "uploaded_at")

    # ✅ Image preview inside admin
    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height: 60px; border-radius: 6px;" />'
        return "-"
    preview.allow_tags = True
    preview.short_description = "Preview"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "year",  # ✅ NEW
        "members",
        "meeting_day",
        "is_alumni",
        "created_by",
        "created_at",
    )

    list_filter = (
        "type",
        "year",  # ✅ NEW
        "is_alumni",
        "meeting_day",
    )

    search_fields = (
        "name",
        "chair",
        "treasurer",
        "secretary",
        "communities",
    )

    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    inlines = [GroupImageInline]

    # ✅ Better navigation for dates
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "type", "year", "slug", "about", "is_alumni")
        }),
        ("Meeting Details", {
            "fields": ("meeting_day", "meeting_time", "meeting_location", "members")
        }),
        ("Leadership", {
            "fields": ("chair", "treasurer", "secretary")
        }),
        ("Communities", {
            "fields": ("communities",)
        }),
        ("Metadata", {
            "fields": ("created_by", "created_at", "updated_at")
        }),
    )

    # ✅ Auto-assign logged-in user
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GroupImage)
class GroupImageAdmin(admin.ModelAdmin):
    list_display = ("group", "order", "uploaded_at", "preview")
    list_filter = ("group",)
    ordering = ("group", "order")
    readonly_fields = ("uploaded_at", "preview")

    # ✅ Image preview here too
    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height: 60px; border-radius: 6px;" />'
        return "-"
    preview.allow_tags = True
    preview.short_description = "Preview"