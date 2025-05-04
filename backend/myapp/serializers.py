from rest_framework import serializers
from .models import (
    Event, WeeklyEventDetails, SingleDayEventDetails, MultiDayEventDetails,
    RsvpSingleDayEventDetails, RsvpMultiDayEventDetails,
    Participant, WeeklyAvailability, DateTimeAvailability, 
    DateAvailability, RsvpStatus, CustomUser
)
import uuid

# --- Event Serializers ---

class EventSerializer(serializers.ModelSerializer):
    event_details = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'location', 'link',
            'coordinator', 'event_type', 'event_details', 'participants'
        ]
        extra_kwargs = {
            'description': {'required': False},
            'location': {'required': False}
        }

    def get_event_details(self, obj):
        if obj.event_type == 'weekly':
            try:
                return WeeklyEventDetailsSerializer(obj.weekly_details).data
            except WeeklyEventDetails.DoesNotExist:
                return None
        elif obj.event_type == 'single_day':
            try:
                return SingleDayEventDetailsSerializer(obj.single_day_details).data
            except SingleDayEventDetails.DoesNotExist:
                return None
        elif obj.event_type == 'multi_day':
            try:
                return MultiDayEventDetailsSerializer(obj.multi_day_details).data
            except MultiDayEventDetails.DoesNotExist:
                return None
        elif obj.event_type == 'rsvp_single':
            try:
                return RsvpSingleDayEventDetailsSerializer(obj.rsvp_single_details).data
            except RsvpSingleDayEventDetails.DoesNotExist:
                return None
        elif obj.event_type == 'rsvp_multi':
            try:
                return RsvpMultiDayEventDetailsSerializer(obj.rsvp_multi_details).data
            except RsvpMultiDayEventDetails.DoesNotExist:
                return None
        return None

    def get_participants(self, obj):
        return ParticipantSerializer(obj.participants.all(), many=True).data

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['coordinator'] = user
        else:
            validated_data['coordinator'] = None

        event_type = validated_data.get('event_type')
        event = Event.objects.create(**validated_data)
        data = self.context['request'].data

        if event_type == 'weekly':
            WeeklyEventDetails.objects.create(
                event=event,
                mon_selected=data.get('mon_selected', False),
                tue_selected=data.get('tue_selected', False),
                wed_selected=data.get('wed_selected', False),
                thur_selected=data.get('thur_selected', False),
                fri_selected=data.get('fri_selected', False),
                sat_selected=data.get('sat_selected', False),
                sun_selected=data.get('sun_selected', False),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
            )
        elif event_type == 'single_day':
            SingleDayEventDetails.objects.create(
                event=event,
                start_date_range=data.get('start_date_range'),
                end_date_range=data.get('end_date_range'),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                is_all_day=data.get('is_all_day', False)
            )
        elif event_type == 'multi_day':
            MultiDayEventDetails.objects.create(
                event=event,
                num_days=data.get('num_days', 1),
                start_date_range=data.get('start_date_range'),
                end_date_range=data.get('end_date_range'),
            )
        elif event_type == 'rsvp_single':
            RsvpSingleDayEventDetails.objects.create(
                event=event,
                date=data.get('date'),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
                is_all_day=data.get('is_all_day', False)
            )
        elif event_type == 'rsvp_multi':
            RsvpMultiDayEventDetails.objects.create(
                event=event,
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                start_time=data.get('start_time'),
                end_time=data.get('end_time'),
            )
        return event

# --- Event Details Serializers (for nested use) ---

class WeeklyEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyEventDetails
        exclude = ['event']

class SingleDayEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleDayEventDetails
        exclude = ['event']

class MultiDayEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiDayEventDetails
        exclude = ['event']

class RsvpSingleDayEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RsvpSingleDayEventDetails
        exclude = ['event']

class RsvpMultiDayEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RsvpMultiDayEventDetails
        exclude = ['event']

# --- Availability Serializers ---

class WeeklyAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyAvailability
        fields = [
            'id', 'participant', 'mon_selected', 'tue_selected', 'wed_selected', 
            'thur_selected', 'fri_selected', 'sat_selected', 'sun_selected',
            'start_time', 'end_time'
        ]

class DateTimeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DateTimeAvailability
        fields = ['id', 'participant', 'selected_date', 'start_time', 'end_time']

class DateAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DateAvailability
        fields = ['id', 'participant', 'selected_date']

class RsvpStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RsvpStatus
        fields = ['id', 'participant', 'status']

# --- Participant Serializer ---

class ParticipantSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'user_first_name', 'user_last_name', 'user_email', 'event']
        read_only_fields = ['id', 'user', 'user_first_name', 'user_last_name', 'user_email']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ParticipantGuestSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(write_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'guest_name', 'event']
        read_only_fields = ['id']

    def create(self, validated_data):
        guest_name = validated_data.pop('guest_name')
        user, _ = CustomUser.objects.get_or_create(
            email=f'guest_{uuid.uuid4().hex[:8]}@guest.com',
            defaults = {
                'first_name': guest_name,
                'is_registered': False,
                'password': CustomUser.objects.make_random_password(),
            }
        )
        return Participant.objects.create(user=user, **validated_data)