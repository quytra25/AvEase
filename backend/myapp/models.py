from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# User manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Extending Django user model
class CustomUser(AbstractUser):
    # first_name, last_name, email, password already included

    username = None  # remove username field
    email = models.EmailField(unique=True)  # make email required + unique
    is_registered = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no extra required fields like username

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Event model
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
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )

    def __str__(self):
        return self.name


# Participant model
class Participant(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} → {self.event.name}"
    

# Availability model
class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    availability_type = models.CharField(
        max_length=15,
        choices=[
            ('weekly', 'Weekly'),
            ('date_time', 'Date & Time'),
            ('date_only', 'Date Only'),
            ('rsvp', 'RSVP Status')
        ]
    )

    def __str__(self):
        return f"{self.user.email} ({self.availability_type})"

# Availability subclasses
class AvailabilityInTheWeek(Availability):
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

class AvailableDateTime(Availability):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

class AvailableDate(Availability):
    date = models.DateField()

class AvailabilityStatus(Availability):
    status = models.CharField(
        max_length=15,
        choices=[('available', 'Available'), ('unavailable', 'Unavailable'), ('tentative', 'Tentative'), ('no_response', 'No Response')]
    )
