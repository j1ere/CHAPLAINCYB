from rest_framework import serializers
from .models import Group, GroupImage


class GroupImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = GroupImage
        fields = ['id', 'image', 'uploaded_at']

    def get_image(self, obj):
        request = self.context.get('request')
        return obj.image.url if obj.image else None

class GroupSerializer(serializers.ModelSerializer):
    images = GroupImageSerializer(many=True, read_only=True)
    community_list = serializers.ListField(child=serializers.CharField(), read_only=True)
    leadership = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'type', 'slug', 'members', 'meeting_time',
            'meeting_day', 'meeting_location', 'communities', 'community_list',
            'chair', 'treasurer', 'secretary', 'leadership', 'about',
            'images', 'is_alumni', 'created_at'
        ]

    def get_leadership(self, obj):
        return obj.leadership


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'name', 'type', 'members', 'meeting_time',
            'meeting_day', 'meeting_location', 'communities',
            'chair', 'treasurer', 'secretary',
            'about', 'is_alumni'
        ]