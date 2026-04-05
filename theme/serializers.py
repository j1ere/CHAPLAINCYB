# theme/serializers.py
from rest_framework import serializers
from .models import Theme

class ThemeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = [
            'id', 'text', 'image', 'image_url', 'year',
            'is_active', 'date_created', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'date_created']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate(self, data):
        # Prevent multiple active themes via API (model already handles it)
        if data.get('is_active') and Theme.objects.filter(is_active=True).exclude(pk=self.instance.pk if self.instance else None).exists():
            # The model save() will handle it, but we can still allow it
            pass
        return data