from django.contrib import admin
from .models import Group, GroupImage


class GroupImageInline(admin.TabularInline):
    model = GroupImage
    extra = 1
    fields = ("image", "order", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "members",
        "meeting_day",
        "meeting_time",
        "is_alumni",
        "created_at",
    )
    list_filter = ("type", "is_alumni", "meeting_day")
    search_fields = ("name", "chair", "treasurer", "secretary", "communities")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    inlines = [GroupImageInline]

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "type", "slug", "about", "is_alumni")
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


@admin.register(GroupImage)
class GroupImageAdmin(admin.ModelAdmin):
    list_display = ("group", "order", "uploaded_at")
    list_filter = ("group",)
    ordering = ("group", "order")