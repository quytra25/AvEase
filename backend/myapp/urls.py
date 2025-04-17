from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ParticipantViewSet, AvailabilityViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
]
