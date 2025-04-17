from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ParticipantViewSet, AvailabilityViewSet, AvailabilityInTheWeekViewSet, AvailableDateTimeViewSet, AvailableDateViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'availabilities', AvailabilityViewSet)
router.register(r'availabilities/weekly', AvailabilityInTheWeekViewSet)
router.register(r'availabilities/datetime', AvailableDateTimeViewSet)
router.register(r'availabilities/date', AvailableDateViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
]
