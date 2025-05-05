from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ViewSets
    EventViewSet, ParticipantViewSet,
    WeeklyAvailabilityViewSet, DateAvailabilityViewSet, RsvpStatusViewSet,

    # Auth & CSRF Views
    csrf_token_view, login_view, signup_view, logout_view, current_user_view,

    # Guest participant creation
    ParticipantGuestCreateView,
)

# DRF router for viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'weekly-availabilities', WeeklyAvailabilityViewSet)
router.register(r'date-availabilities', DateAvailabilityViewSet)
router.register(r'rsvp-statuses', RsvpStatusViewSet)

# Final URL patterns
urlpatterns = [
    path('', include(router.urls)),

    # Guest join (no auth required)
    path('participants/guest/', ParticipantGuestCreateView.as_view(), name='guest-participant-create'),

    # CSRF setup
    path('csrf/', csrf_token_view, name='csrf-token'),

    # Auth endpoints
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('current-user/', current_user_view, name='current-user'),
]