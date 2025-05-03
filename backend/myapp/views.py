from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Event, Participant, WeeklyAvailability, DateTimeAvailability, DateAvailability, RsvpStatus
)
from .serializers import (
    EventSerializer, ParticipantSerializer, ParticipantGuestSerializer,
    WeeklyAvailabilitySerializer, DateTimeAvailabilitySerializer, DateAvailabilitySerializer, RsvpStatusSerializer
)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'link'

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        event = self.get_object()
        participants = event.participants.all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availabilities(self, request, pk=None):
        event = self.get_object()
        participant_ids = event.participants.values_list('id', flat=True)
        return Response({
            'weekly': WeeklyAvailabilitySerializer(WeeklyAvailability.objects.filter(participant_id__in=participant_ids), many=True).data,
            'datetime': DateTimeAvailabilitySerializer(DateTimeAvailability.objects.filter(participant_id__in=participant_ids), many=True).data,
            'date': DateAvailabilitySerializer(DateAvailability.objects.filter(participant_id__in=participant_ids), many=True).data,
            'rsvp': RsvpStatusSerializer(RsvpStatus.objects.filter(participant_id__in=participant_ids), many=True).data,
        })

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ParticipantGuestCreateView(generics.CreateAPIView):
    serializer_class = ParticipantGuestSerializer
    permission_classes = [permissions.AllowAny]

class WeeklyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = WeeklyAvailability.objects.all()
    serializer_class = WeeklyAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

class DateTimeAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DateTimeAvailability.objects.all()
    serializer_class = DateTimeAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

class DateAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DateAvailability.objects.all()
    serializer_class = DateAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

class RsvpStatusViewSet(viewsets.ModelViewSet):
    queryset = RsvpStatus.objects.all()
    serializer_class = RsvpStatusSerializer
    permission_classes = [permissions.AllowAny]