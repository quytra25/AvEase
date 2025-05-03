from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    EventViewSet, ParticipantViewSet, ParticipantGuestCreateView,
    WeeklyAvailabilityViewSet, DateTimeAvailabilityViewSet, DateAvailabilityViewSet, RsvpStatusViewSet
)
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'weekly-availabilities', WeeklyAvailabilityViewSet)
router.register(r'datetime-availabilities', DateTimeAvailabilityViewSet)
router.register(r'date-availabilities', DateAvailabilityViewSet)
router.register(r'rsvp-statuses', RsvpStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('participants/guest/', ParticipantGuestCreateView.as_view(), name='guest-participant-create'),
    path('csrf/', csrf),
]