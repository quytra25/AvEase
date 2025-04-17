from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, Participant, Availability
from .serializers import EventSerializer, ParticipantSerializer, AvailabilitySerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

def home(request):
    return HttpResponse("Hello World!")