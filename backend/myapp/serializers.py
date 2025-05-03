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
    """
    Serializer for the base Event model with methods to handle different event types
    """
    
    event_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'link', 'coordinator', 'event_type', 'event_details']
        extra_kwargs = {
            'description': {'required': False},
            'location': {'required': False}
        }
    
    def get_event_details(self, obj):
        """Return the appropriate event details based on event_type"""
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
    
    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['coordinator'] = user
        else:
            validated_data['coordinator'] = None

        event_type = validated_data.get('event_type')
        details_data = self.initial_data.get('event_details', {})
        
        # Create the base event
        event = Event.objects.create(**validated_data)
        
        # Create the appropriate event details based on event_type
        if event_type == 'weekly' and details_data:
            WeeklyEventDetails.objects.create(event=event, **details_data)
        elif event_type == 'single_day' and details_data:
            SingleDayEventDetails.objects.create(event=event, **details_data)
        elif event_type == 'multi_day' and details_data:
            MultiDayEventDetails.objects.create(event=event, **details_data)
        elif event_type == 'rsvp_single' and details_data:
            RsvpSingleDayEventDetails.objects.create(event=event, **details_data)
        elif event_type == 'rsvp_multi' and details_data:
            RsvpMultiDayEventDetails.objects.create(event=event, **details_data)
        
        return event
    
    def update(self, instance, validated_data):
        event_type = validated_data.get('event_type', instance.event_type)
        details_data = self.initial_data.get('event_details', {})
        
        # Update the base event
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update the appropriate event details based on event_type
        if event_type == 'weekly' and details_data:
            weekly_details, created = WeeklyEventDetails.objects.get_or_create(event=instance)
            for attr, value in details_data.items():
                setattr(weekly_details, attr, value)
            weekly_details.save()

        elif event_type == 'single_day' and details_data:
            single_day_details, created = SingleDayEventDetails.objects.get_or_create(event=instance)
            for attr, value in details_data.items():
                setattr(single_day_details, attr, value)
            single_day_details.save()

        elif event_type == 'multi_day' and details_data:
            multi_day_details, created = MultiDayEventDetails.objects.get_or_create(event=instance)
            for attr, value in details_data.items():
                setattr(multi_day_details, attr, value)
            multi_day_details.save()

        elif event_type == 'rsvp_single' and details_data:
            rsvp_single_details, created = RsvpSingleDayEventDetails.objects.get_or_create(event=instance)
            for attr, value in details_data.items():
                setattr(rsvp_single_details, attr, value)
            rsvp_single_details.save()
            
        elif event_type == 'rsvp_multi' and details_data:
            rsvp_multi_details, created = RsvpMultiDayEventDetails.objects.get_or_create(event=instance)
            for attr, value in details_data.items():
                setattr(rsvp_multi_details, attr, value)
            rsvp_multi_details.save()
        
        return instance

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
            defaults={
                'first_name': guest_name,
                'is_registered': False,
                'password': CustomUser.objects.make_random_password(),
            }
        )
        return Participant.objects.create(user=user, **validated_data)