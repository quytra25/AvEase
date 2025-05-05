from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid

# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------

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

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_registered = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

# ---------------------------------------------------
# EVENT MODELS
# ---------------------------------------------------

class Event(models.Model):
    """Base Event Model with shared fields"""
    EVENT_TYPE_CHOICES = [
        ('weekly_match', 'Weekly Availability Match'),
        ('date_match', 'Date Availability Match'),
        ('rsvp_single', 'RSVP Single-Day'),
        ('rsvp_multi', 'RSVP Multi-Day'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='coordinated_events'
    )
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"

class WeeklyEventDetails(models.Model):
    """Weekly recurring event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='weekly_details')
    mon_selected = models.BooleanField(default=False)
    tue_selected = models.BooleanField(default=False)
    wed_selected = models.BooleanField(default=False)
    thur_selected = models.BooleanField(default=False)
    fri_selected = models.BooleanField(default=False)
    sat_selected = models.BooleanField(default=False)
    sun_selected = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        days = []
        if self.mon_selected: days.append('Mon')
        if self.tue_selected: days.append('Tue')
        if self.wed_selected: days.append('Wed')
        if self.thur_selected: days.append('Thur')
        if self.fri_selected: days.append('Fri')
        if self.sat_selected: days.append('Sat')
        if self.sun_selected: days.append('Sun')
        return f"{', '.join(days)} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
    
class DateAvailabilityEventDetails(models.Model):
    """Availability in dates event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='date_match_details')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.event.name} — {self.start_date} to {self.end_date}"

class RsvpSingleDayEventDetails(models.Model):
    """RSVP Single day event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='rsvp_single_details')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_all_day = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.date} ({self.start_time}-{self.end_time})"

class RsvpMultiDayEventDetails(models.Model):
    """RSVP Multi-day event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='rsvp_multi_details')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_all_day = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.start_date} to {self.end_date}"

# ---------------------------------------------------
# PARTICIPANT MODEL
# ---------------------------------------------------

class Participant(models.Model):
    """User participation in events"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    
    class Meta:
        unique_together = ['user', 'event']
    
    def __str__(self):
        return f"{self.user.email} - {self.event.name}"

# ---------------------------------------------------
# AVAILABILITY MODELS
# ---------------------------------------------------
class WeeklyAvailability(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='weekly_availabilities')
    selected_day = models.CharField(max_length=10, default='mon', choices=[
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thur', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ])
    selected_start_time = models.TimeField()

    class Meta:
        unique_together = ('participant', 'selected_day', 'selected_start_time')

    def __str__(self):
        return f"{self.participant} - {self.selected_day} at {self.selected_start_time.strftime('%H:%M')}"


class DateAvailability(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='date_availabilities'
    )
    selected_date = models.DateField()

    class Meta:
        unique_together = ['participant', 'selected_date']
        verbose_name_plural = 'Date availabilities'

    def __str__(self):
        return f"{self.participant} - {self.selected_date}"


class RsvpStatus(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='rsvp_statuses'
    )
    RSVP_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('tentative', 'Tentative'),
        ('no_response', 'No Response'),
    ]
    status = models.CharField(max_length=15, choices=RSVP_CHOICES, default='no_response')

    class Meta:
        verbose_name_plural = 'RSVP statuses'

    def __str__(self):
        return f"{self.participant.user} - {self.status}"