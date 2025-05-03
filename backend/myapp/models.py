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
        ('weekly', 'Weekly Event'),
        ('single_day', 'Single Day Event'),
        ('multi_day', 'Multi Day Event'),
        ('rsvp_single', 'RSVP Single Day Event'),
        ('rsvp_multi', 'RSVP Multi Day Event'),
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

class SingleDayEventDetails(models.Model):
    """Single day event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='single_day_details')
    start_date_range = models.DateField()
    end_date_range = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_all_day = models.BooleanField(default=False)
    confirmed_date = models.DateField(null=True, blank=True)
    confirmed_start_time = models.TimeField(null=True, blank=True)
    confirmed_end_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        if self.confirmed_date:
            return f"{self.confirmed_date} ({self.confirmed_start_time}-{self.confirmed_end_time})"
        return f"Range: {self.start_date_range} to {self.end_date_range}"

class MultiDayEventDetails(models.Model):
    """Multi-day event details"""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='multi_day_details')
    num_days = models.PositiveIntegerField()
    start_date_range = models.DateField()
    end_date_range = models.DateField()
    confirmed_start_date = models.DateField(null=True, blank=True)
    confirmed_end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        if self.confirmed_start_date:
            return f"{self.confirmed_start_date} to {self.confirmed_end_date}"
        return f"Range: {self.start_date_range} to {self.end_date_range}"

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
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='weekly_availabilities'
    )
    mon_selected = models.BooleanField(default=False)
    tue_selected = models.BooleanField(default=False)
    wed_selected = models.BooleanField(default=False)
    thur_selected = models.BooleanField(default=False)
    fri_selected = models.BooleanField(default=False)
    sat_selected = models.BooleanField(default=False)
    sun_selected = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ['participant', 'start_time', 'end_time']
        verbose_name_plural = 'Weekly availabilities'

    def __str__(self):
        days = [day for day, selected in zip(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            [self.mon_selected, self.tue_selected, self.wed_selected, self.thur_selected,
             self.fri_selected, self.sat_selected, self.sun_selected]
        ) if selected]
        return f"{self.participant.user.email} - {', '.join(days)} ({self.start_time}-{self.end_time})"


class DateTimeAvailability(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='datetime_availabilities'
    )
    selected_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ['participant', 'selected_date', 'start_time', 'end_time']
        verbose_name_plural = 'Date-time availabilities'

    def __str__(self):
        return f"{self.participant.user.email} - {self.selected_date} ({self.start_time}-{self.end_time})"


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
        return f"{self.participant.user.email} - {self.selected_date}"


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
        return f"{self.participant.user.email} - {self.get_status_display()}"