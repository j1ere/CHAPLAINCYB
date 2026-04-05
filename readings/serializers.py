# calendar/serializers.py
from rest_framework import serializers
from .models import CalendarEntry

class CalendarEntrySerializer(serializers.ModelSerializer):
    readings = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        required=False
    )

    class Meta:
        model = CalendarEntry
        fields = [
            'id', 'date', 'event', 'type', 'readings', 
            'verse', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by']

    def validate_readings(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Readings must be a list")
        return value
    


# serializers.py
from rest_framework import serializers
from .models import Prayer

class PrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prayer
        fields = ['id', 'name', 'content']