from django.contrib import admin
from .models import Venue, MyClubUser, Event
from django.contrib.auth.models import Group

# Register your models here.
# admin.site.register(Venue)
admin.site.register(MyClubUser)
# admin.site.register(Event)

#Remove groups
admin.site.unregister(Group)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date',)