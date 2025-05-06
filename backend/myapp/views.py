from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .models import (
    Event, Participant, CustomUser,
    WeeklyAvailability, DateAvailability, RsvpStatus
)

from .serializers import (
    EventSerializer, ParticipantSerializer, ParticipantGuestSerializer,
    WeeklyAvailabilitySerializer, DateAvailabilitySerializer, RsvpStatusSerializer
)


# CSRF Token Setter
@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    data = request.data
    if CustomUser.objects.filter(email=data['email']).exists():
        return JsonResponse({'error': 'Email already in use'}, status=400)

    user = CustomUser.objects.create_user(
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    login(request, user)
    return JsonResponse({'message': 'User created', 'user': {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful', 'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }})
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

@api_view(['GET'])
def current_user_view(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    return JsonResponse({'user': None})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_events(request):
    user = request.user
    created_events = Event.objects.filter(coordinator=user)
    joined_events = Event.objects.filter(participants__user=user).distinct()

    data = {
        'created': EventSerializer(created_events, many=True).data,
        'joined': EventSerializer(joined_events, many=True).data,
    }
    return Response(data)

# Guest Join
@method_decorator(csrf_exempt, name='dispatch')
class ParticipantGuestCreateView(generics.CreateAPIView):
    serializer_class = ParticipantGuestSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


# Event ViewSet
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
    def availabilities(self, request, **kwargs):
        event = self.get_object()
        participant_ids = event.participants.values_list('id', flat=True)

        return Response({
            'weekly_match': WeeklyAvailabilitySerializer(
                WeeklyAvailability.objects.filter(participant_id__in=participant_ids), many=True
            ).data,
            'date_match': DateAvailabilitySerializer(
                DateAvailability.objects.filter(participant_id__in=participant_ids), many=True
            ).data,
            'rsvp': RsvpStatusSerializer(
                RsvpStatus.objects.filter(participant_id__in=participant_ids), many=True
            ).data,
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.coordinator:
            return Response({'detail': 'You are not allowed to delete this event.'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        created_events = Event.objects.filter(coordinator=user)
        joined_events = Event.objects.filter(participants__user=user).exclude(coordinator=user).distinct()
        return Response({
            'created': EventSerializer(created_events, many=True).data,
            'joined': EventSerializer(joined_events, many=True).data
        })


# Participant ViewSet
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Availability ViewSets
class WeeklyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = WeeklyAvailability.objects.all()
    serializer_class = WeeklyAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_availability(self, request):
        data = request.data
        participant_id = data.get('participant')
        selected_day = data.get('selected_day')
        selected_start_time = data.get('selected_start_time')

        try:
            availability = WeeklyAvailability.objects.get(
                participant_id=participant_id,
                selected_day=selected_day,
                selected_start_time=selected_start_time
            )
            availability.delete()
            return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except WeeklyAvailability.DoesNotExist:
            return Response({'error': 'Availability not found'}, status=status.HTTP_404_NOT_FOUND)

class DateAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DateAvailability.objects.all()
    serializer_class = DateAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='remove')
    def delete(self, request):
        participant_id = request.data.get('participant')
        DateAvailability.objects.filter(participant_id=participant_id).delete()
        return Response({'status': 'deleted'})

class RsvpStatusViewSet(viewsets.ModelViewSet):
    queryset = RsvpStatus.objects.all()
    serializer_class = RsvpStatusSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        participant = request.data.get('participant')
        status_value = request.data.get('status')

        try:
            instance = RsvpStatus.objects.get(participant=participant)
            instance.status = status_value
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RsvpStatus.DoesNotExist:
            return super().create(request, *args, **kwargs)