from rest_framework import serializers
from .models import Attendee, Event

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'name', 'email']  # Include only necessary fields

class EventSerializer(serializers.ModelSerializer):
    attendees = AttendeeSerializer(many=True, read_only=True)  # Nest attendees here

    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'description', 'location', 'attendees']  # Include the attendees
