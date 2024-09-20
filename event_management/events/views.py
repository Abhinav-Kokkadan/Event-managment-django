from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Event, Attendee
from .forms import EventForm, AttendeeForm
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .serializers import EventSerializer, AttendeeSerializer
from django.http import JsonResponse  # For returning JSON response
from datetime import datetime
import django_filters
from rest_framework import generics

class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer



# HTML-based views

def event_list(request):
    events = Event.objects.all().order_by('-id')  # Order by primary key in descending order
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            attendee.save()
            return redirect('event_detail', pk=pk)
    else:
        form = AttendeeForm()
    return render(request, 'events/register.html', {'form': form, 'event': event})

def date_sort(request, date=None):
    if date:
        try:
            # Convert the string date from URL into a datetime object
            event_date = datetime.strptime(date, "%Y-%m-%d").date()

            # Fetch the total capacity of events happening on the given date
            events_on_date = Event.objects.filter(date=event_date).aggregate(total_capacity=Sum('capacity'))

            # If there are no events on that date, return 0 capacity
            total_capacity = events_on_date['total_capacity'] or 0

            return JsonResponse({'date': date, 'total_capacity': total_capacity})
        
        except ValueError:
            # Handle invalid date format
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
    
    else:
        # Fetch all events and aggregate total capacity per date
        events = Event.objects.values('date').annotate(total_capacity=Sum('capacity'))

        # Convert to dictionary format
        result = {event['date'].strftime('%Y-%m-%d'): event['total_capacity'] for event in events}
        
        return JsonResponse(result)

# Define the filter set
class AttendeeFilterSet(django_filters.FilterSet):
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = Attendee
        fields = ['email']

# DRF-based views (for API handling)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()  # Default queryset, no sorting here
    serializer_class = EventSerializer

    # Adding filter and ordering backends
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Adding ordering filter
    ordering_fields = ['capacity','id']  # Allow sorting by 'capacity'
    ordering = ['-capacity','-id']  # Default order (descending by capacity)


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all().order_by('-id')
    serializer_class = AttendeeSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AttendeeFilterSet
    ordering_fields = ['email']  # Optional: Allow sorting by email
    ordering = ['email']  # Optional: Default ordering by email

