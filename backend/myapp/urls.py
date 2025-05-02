from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ParticipantViewSet, AvailabilityViewSet, get_csrf_token
from django.urls import path

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'participants', ParticipantViewSet, basename='participant')
router.register(r'availabilities', AvailabilityViewSet, basename='availability')

urlpatterns = router.urls + [
    path('csrf/', get_csrf_token, name='get_csrf_token'),
]