#import forms
from django import forms
#import modelForm
from django.forms import ModelForm
#import models
from .models import Venue, Event


#create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image']

        #add labels
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': '',
        }

        #add widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip/Postal Code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Phone'}),
            'web': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Website Address'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'venue_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


#Admin superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'manager', 'attendees', 'description']

        #add labels
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }

        #add widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Description'}),
        }
        

#User event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'venue', 'attendees', 'description']

        #add labels
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }

        #add widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control' , 'placeholder': 'Description'}),
        }