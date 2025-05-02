import uuid
from rest_framework import serializers
from .models import (
    Event, Participant, CustomUser, Availability,
    AvailabilityMatchEvent, RsvpBasedEvent,
    WeeklyEvent, SingleDayEvent, MultiDayEvent,
    RsvpSingleDayEvent, RsvpMultiDayEvent,
    AvailabilityInTheWeek, AvailableDateTime, AvailableDate, AvailabilityStatus
)


# Base Event serializer: hide coordinator & link on input, default coordinator to request.user
class EventSerializer(serializers.ModelSerializer):
    coordinator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    link = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'type', 'description', 'location', 'coordinator', 'link'
        ]
        read_only_fields = ['id', 'link']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['coordinator'] = request.user
        else:
            validated_data.pop('coordinator', None)
        return super().create(validated_data)

# EventDetail with nested participants
class EventDetailSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'type', 'description', 'location', 'link', 'participants'

            # 'id', 'name', 'description', 'type', 'sub_type', 'link', 'is_all_day',
            # # availability-match fields
            # 'start_date_range', 'end_date_range', 'start_time', 'end_time',
            # # RSVP-based fields
            # 'date', 'start_date', 'end_date',
            # 'participants'
        ]
        read_only_fields = fields

    def get_participants(self, obj):
        from .serializers import ParticipantSerializer
        return ParticipantSerializer(obj.participant_set.all(), many=True).data

# Detailed Event view: includes participants + availabilities
class AvailabilityInTheWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityInTheWeek
        fields = ['id', 'participant', 'selected_day', 'selected_start_time', 'selected_end_time']

class AvailableDateTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDateTime
        fields = ['id', 'participant', 'selected_date', 'selected_start_time', 'selected_end_time']

class AvailableDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDate
        fields = ['id', 'participant', 'selected_date']

class AvailabilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityStatus
        fields = ['id', 'participant', 'rsvp_status']

class AvailabilitySerializer(serializers.ModelSerializer):
    """
    Polymorphic serializer: picks the right subtype based on availability_type
    """
    def to_representation(self, instance):
        # dispatch to the correct child serializer
        if isinstance(instance, AvailabilityInTheWeek):
            return AvailabilityInTheWeekSerializer(instance).data
        if isinstance(instance, AvailableDateTime):
            return AvailableDateTimeSerializer(instance).data
        if isinstance(instance, AvailableDate):
            return AvailableDateSerializer(instance).data
        if isinstance(instance, AvailabilityStatus):
            return AvailabilityStatusSerializer(instance).data
        return super().to_representation(instance)

    class Meta:
        model = Availability
        fields = ['id', 'participant', 'availability_type']

class ParticipantSerializer(serializers.ModelSerializer):
    # includes nested availabilities
    availabilities = AvailabilitySerializer(many=True, read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'user_first_name', 'user_last_name', 'event', 'availabilities']
        read_only_fields = ['id', 'user', 'user_first_name', 'user_last_name']

    def create(self, validated_data):
        # automatically assign the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class ParticipantGuestSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(write_only=True)

    class Meta:
        model = Participant
        fields = ['id','event','guest_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        name = validated_data.pop('guest_name')
        # create or fetch a “guest” user with that name
        user, _ = CustomUser.objects.get_or_create(
            first_name=name,
            username=f"guest_{uuid.uuid4().hex[:8]}",  # unique placeholder
            defaults={'is_registered': False}
        )
        return Participant.objects.create(user=user, **validated_data)