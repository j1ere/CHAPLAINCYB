# events/serializers.py
from rest_framework import serializers
from .models import UpcomingEvent, RegularEvent, CalendarFile


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

# class CalendarFileSerializer(serializers.ModelSerializer):
#     # file_url = serializers.SerializerMethodField()

#     class Meta:
#         model = CalendarFile
#         fields = ['id', 'file_type', 'file', 'file_url', 'uploaded_at']
#         read_only_fields = ['uploaded_at']

#     # def get_file_url(self, obj):
#     #     if obj.file:
#     #         request = self.context.get('request')
#     #         if request:
#     #             return request.build_absolute_uri(obj.file.url)
#     #         # Fallback: hardcode the backend base URL if no request context
#     #         # return f"http://localhost:8000{obj.file.url}"
#     #     return None
    


class CalendarFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarFile
        fields = ['id', 'file_type', 'file_url', 'uploaded_at']
        read_only_fields = ['uploaded_at']


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