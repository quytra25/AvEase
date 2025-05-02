from rest_framework import viewsets, permissions
from django.db import models
from django.core.exceptions import PermissionDenied
from .models import Event, Participant, Availability
from .serializers import (
    EventSerializer, EventDetailSerializer, ParticipantSerializer, ParticipantGuestSerializer, AvailabilitySerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Event.objects.filter(
                models.Q(coordinator=user) | models.Q(participant__user=user)
            ).distinct()
        return Event.objects.none()

    def perform_update(self, serializer):
        event = self.get_object()
        if event.coordinator != self.request.user:
            raise PermissionDenied("Only the coordinator can edit this event.")
        serializer.save()

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # auto‐assign the user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='guest')
    def join_guest(self, request):
        ser = ParticipantGuestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        p = ser.save()
        return Response({'id': p.id})

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        participant = serializer.validated_data['participant']
        if participant.user != self.request.user:
            raise PermissionDenied("Can't set someone else's availability.")
        serializer.save()