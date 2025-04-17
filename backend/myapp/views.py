from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, Participant, Availability, AvailabilityInTheWeek, AvailableDateTime, AvailableDate
from .serializers import EventSerializer, ParticipantSerializer, AvailabilitySerializer, AvailabilityInTheWeekSerializer, AvailableDateTimeSerializer, AvailableDateSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class AvailabilityInTheWeekViewSet(viewsets.ModelViewSet):
    queryset = AvailabilityInTheWeek.objects.all()
    serializer_class = AvailabilityInTheWeekSerializer

class AvailableDateTimeViewSet(viewsets.ModelViewSet):
    queryset = AvailableDateTime.objects.all()
    serializer_class = AvailableDateTimeSerializer

class AvailableDateViewSet(viewsets.ModelViewSet):
    queryset = AvailableDate.objects.all()
    serializer_class = AvailableDateSerializer

def home(request):
    return HttpResponse("Hello World!")