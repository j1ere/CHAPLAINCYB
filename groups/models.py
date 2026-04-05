from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Group(models.Model):
    TYPE_CHOICES = [
        ("Prayer House", "Prayer House"),
        ("Movement", "Movement"),
        ("Year Group", "Year Group"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="Prayer House")
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    members = models.CharField(max_length=50, blank=True)
    meeting_time = models.CharField(max_length=100, blank=True)
    meeting_day = models.CharField(max_length=50, blank=True)
    meeting_location = models.CharField(max_length=200, blank=True)

    communities = models.TextField(blank=True)
    chair = models.CharField(max_length=150, blank=True)
    treasurer = models.CharField(max_length=150, blank=True)
    secretary = models.CharField(max_length=150, blank=True)

    about = models.TextField(blank=True)
    is_alumni = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_groups"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Group.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def community_list(self):
        return [c.strip() for c in self.communities.split(",") if c.strip()]

    @property
    def leadership(self):
        leaders = []
        if self.chair:
            leaders.append(f"Chair: {self.chair}")
        if self.treasurer:
            leaders.append(f"Treasurer: {self.treasurer}")
        if self.secretary:
            leaders.append(f"Secretary: {self.secretary}")
        return leaders


class GroupImage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="group_gallery/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "uploaded_at"]

    def __str__(self):
        return f"Image for {self.group.name}"