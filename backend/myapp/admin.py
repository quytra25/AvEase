from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Event, Participant,
    WeeklyEventDetails, SingleDayEventDetails, MultiDayEventDetails,
    RsvpSingleDayEventDetails, RsvpMultiDayEventDetails,
    WeeklyAvailability, DateTimeAvailability, DateAvailability, RsvpStatus
)

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'is_registered')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'is_registered', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_registered', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Inline Event Details
class WeeklyEventDetailsInline(admin.StackedInline):
    model = WeeklyEventDetails
    extra = 0

class SingleDayEventDetailsInline(admin.StackedInline):
    model = SingleDayEventDetails
    extra = 0

class MultiDayEventDetailsInline(admin.StackedInline):
    model = MultiDayEventDetails
    extra = 0

class RsvpSingleDayEventDetailsInline(admin.StackedInline):
    model = RsvpSingleDayEventDetails
    extra = 0

class RsvpMultiDayEventDetailsInline(admin.StackedInline):
    model = RsvpMultiDayEventDetails
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'coordinator', 'link')
    list_filter = ('event_type',)
    search_fields = ('name',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        inlines = {
            'weekly': WeeklyEventDetailsInline,
            'single_day': SingleDayEventDetailsInline,
            'multi_day': MultiDayEventDetailsInline,
            'rsvp_single': RsvpSingleDayEventDetailsInline,
            'rsvp_multi': RsvpMultiDayEventDetailsInline,
        }
        inline_class = inlines.get(obj.event_type)
        return [inline_class(self.model, self.admin_site)] if inline_class else []

admin.site.register(Participant)
admin.site.register(WeeklyAvailability)
admin.site.register(DateTimeAvailability)
admin.site.register(DateAvailability)
admin.site.register(RsvpStatus)