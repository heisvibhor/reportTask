from rest_framework import serializers
from .models import Reports

class  EventsSerializer(serializers.Serializer):
    type = serializers.CharField()
    created_time = serializers.DateTimeField()
    unit = serializers.IntegerField()

class EventsCollectionSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    student_id = serializers.UUIDField()
    events = EventsSerializer(many=True)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
