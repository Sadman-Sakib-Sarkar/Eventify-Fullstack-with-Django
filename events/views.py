from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
import pytz
from .models import Event, Venue
# import user model from django
from django.contrib.auth.models import User
#import venue form
from .forms import VenueForm, EventForm, EventFormAdmin
#import http response redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse #filereponse is used for pdf
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

from django.contrib import messages

#import pagination stuff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#get current datetime of dhaka bangladesh
tz = pytz.timezone('Asia/Dhaka')

# Create your views here.
def home(request, year=datetime.now(tz).year, month=datetime.now(tz).strftime('%B')):
    name = 'Sadman'
    month_num = list(calendar.month_name).index(month.capitalize())
    month_num = int(month_num)

    #create a calendar
    # cal = HTMLCalendar().formatmonth(year, month_num)
    cal = HTMLCalendar().monthdays2calendar(year, month_num)


    #get current year
    now = datetime.now(tz)
    current_year = now.year

    #query the events model for dates
    event_list = Event.objects.filter(event_date__year = year, event_date__month = month_num)

    #get current month
    current_month = now.strftime('%B')

    #get current time
    current_time = now.strftime('%I:%M %p')
    
    return render(request,
                  'events/home.html', {
                      'name': name, 
                      'year': year, 
                      'month': month.title(), 
                      'month_num': month_num,
                      'cal': cal,
                      'current_year': current_year,
                      'current_month': current_month,
                      'current_time': current_time,
                      'event_list': event_list,
                      })


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date') #if we want random order we can use .order_by('?')
    
    return render(request, 'events/event_list.html', {'event_list': event_list})


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES) #request.FILES is used to upload files
        if form.is_valid():
            #automatic save owner id with the current user id
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})

def list_venues(request):
    # venue_list = Venue.objects.all() #if we want random order we can use .order_by('?')

    #set up pagingation
    paginator = Paginator(Venue.objects.all(), 3) #show 3 venues per page
    page = request.GET.get('page')
    venues = paginator.get_page(page)

    return render(request, 'events/venue.html', {'venues': venues})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues,})
    else:
    #     search_text = ''

    # venue_list = Venue.objects.filter(name__contains=search_text)
        return render(request, 'events/search_venues.html')
    


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue) #request.FILES is used to upload files

    # if request.method == 'POST':
    #     form = VenueForm(request.POST, instance=venue)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/list_venues')

    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})



def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event/?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event/?submitted=True')
    else:
        #Just going to the page not submitting
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    # if request.method == 'POST':
    #     form = VenueForm(request.POST, instance=venue)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/events')

    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager: 
        event.delete()
        messages.success(request, ('Event has been deleted!'))
        return HttpResponseRedirect('/events')
    else:
        messages.error(request, ('You are not authorized to delete this event!'))
        return HttpResponseRedirect('/events')

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return HttpResponseRedirect('/list_venues')


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venue_list.txt"'

    venues = Venue.objects.all()

    #Example of writing to a text file manually
    #lines = ["This is line 1\n",
    #         "This is line 2\n",
    #         "This is line 3\n"]
    #response.writelines(lines)
    #return response

    for venue in venues:
        response.write(venue.name + '\n')
        response.write(venue.address + '\n')
        response.write(venue.zip_code + '\n')
        response.write(venue.phone + '\n')
        response.write(venue.web + '\n')
        response.write(venue.email_address + '\n\n')

    return response


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venue_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['SL No.','Venue Name', 'Address', 'Zip Code', 'Phone', 'Website', 'Email Address'])

    venues = Venue.objects.all()

    cnt = 1
    for venue in venues:
        writer.writerow([cnt, venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
        cnt += 1

    return response


def venue_pdf(request):
    # we need to install reportlab for this by running the command: pip install reportlab
    # then import the following
    # from reportlab.pdfgen import canvas
    # from reportlab.lib.pagesizes import letter
    # from reportlab.lib.units import inch

    #create bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    #Add some line of text
    # lines = [
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]

    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append('------------------------')

    for line in lines:
        textob.textLine(line)

    #finish the text object
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue_list.pdf')



def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.error(request, ('You are not logged in!'))
        return HttpResponseRedirect('/login')
    

def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events})
    else:
    #     search_text = ''

    # venue_list = Venue.objects.filter(name__contains=search_text)
        return render(request, 'events/search_events.html')
    


def admin_approval(request):
    #Get counts of events, venues, and users
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')

    if request.user.is_superuser:
        if request.method == 'POST':
            # event_id = request.POST.get('event_id')
            # event = Event.objects.get(pk=event_id)
            # event.approved = True
            # event.save()
            id_list = request.POST.getlist('boxes')
            
            #uncheck all events
            for event in event_list:
                event.approved = False
                event.save()
            #update the database
            for i in id_list:
                event = Event.objects.get(pk=int(i))
                event.approved = True
                event.save()

            messages.success(request, ('Event has been updated!'))
            return HttpResponseRedirect('/events')
            
        else:
            return render(request, 'events/admin_approval.html', {'event_list': event_list, 'event_count': event_count, 'venue_count': venue_count, 'user_count': user_count})
        
    else:
        messages.error(request, ('You are not authorized to view this page!'))
        return HttpResponseRedirect('/events')

    