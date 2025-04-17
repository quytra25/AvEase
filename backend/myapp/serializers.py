from rest_framework import serializers
from .models import Event, Participant, Availability, AvailabilityInTheWeek, AvailableDateTime, AvailableDate

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class AvailabilityInTheWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityInTheWeek
        fields = '__all__'

class AvailableDateTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDateTime
        fields = '__all__'

class AvailableDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDate
        fields = '__all__'