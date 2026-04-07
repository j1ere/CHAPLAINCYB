# events/serializers.py
from rest_framework import serializers
from .models import UpcomingEvent, RegularEvent, CalendarFile

from cloudinary.utils import cloudinary_url

# class CalendarFileSerializer(serializers.ModelSerializer):
#     file_url = serializers.SerializerMethodField()

#     class Meta:
#         model = CalendarFile
#         fields = ['id', 'file_type', 'file', 'file_url', 'uploaded_at']
#         read_only_fields = ['uploaded_at']

#     def get_file_url(self, obj):
#         if obj.file:
#             return obj.file.url
#         return None

class CalendarFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = CalendarFile
        fields = ['id', 'file_type', 'file', 'file_url', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def get_file_url(self, obj):
        if obj.file:
            url, options = cloudinary_url(
                obj.file.name,
                resource_type="raw",
                type="authenticated",  # required for raw files
                sign_url=True,         # generates a signed URL
                expires=600            # valid for 10 minutes
            )
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(url)
            return url
            # Fallback: hardcode the backend base URL if no request context
            # return f"http://localhost:8000{obj.file.url}"
        return None
    

class UpcomingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingEvent
        fields = '__all__'
        read_only_fields = ['created_by']


class RegularEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularEvent
        fields = '__all__'
        read_only_fields = ['created_by']