# events/serializers.py
from rest_framework import serializers
from .models import UpcomingEvent, RegularEvent, CalendarFile



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