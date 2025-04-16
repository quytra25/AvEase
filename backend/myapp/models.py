from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    event_type = [
        ('weekly', 'Weekly'),
        ('single', 'Single-Day'),
        ('multi', 'Multi-Day'),
        ('rsvp_single', 'RSVP Single-Day'),
        ('rsvp_multi', 'RSVP Multi-Day'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=event_type)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

