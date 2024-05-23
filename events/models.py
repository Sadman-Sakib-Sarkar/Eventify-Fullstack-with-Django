from django.db import models
#import user model
from django.contrib.auth.models import User

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip/Postal Code', max_length=12)
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, null=True, default=1)
    venue_image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    # attendees = models.ManyToManyField(MyClubUser, blank=True)
    # attendees = models.ManyToManyField(User, blank=True)
    attendees = models.ManyToManyField(User, blank=True, related_name='event_attendees')
    approved = models.BooleanField('Approved', default=False)


    def __str__(self):
        return self.name
    

    @property
    def DaysToEvent(self):
        from datetime import date
        event_date = self.event_date.date()
        current_date = date.today()
        days_to_event = (event_date - current_date).days
        return days_to_event
    
    @property
    def IsPastEvent(self):
        from datetime import date
        event_date = self.event_date.date()
        current_date = date.today()

        if event_date > current_date:
            return "Upcoming"
        else:
            return "Past"

