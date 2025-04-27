from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event, Participant, Availability

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal info', {'fields': ('first_name','last_name','is_registered')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','is_registered','password1','password2'),
        }),
    )
    list_display = ('email','first_name','last_name','is_registered','is_staff')
    search_fields = ('email','first_name','last_name')
    ordering = ('email',)

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Availability)