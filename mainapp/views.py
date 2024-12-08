from django.views.generic import FormView, DetailView, ListView, CreateView , UpdateView , View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Flight, Booking
from .forms import SearchFlightForm, BookingForm
from django.utils import timezone
from django.http import HttpResponseForbidden


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = SearchFlightForm

    def form_valid(self, form):
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        return redirect('flight-list', source=source, destination=destination)

class FlightListView(ListView):
    model = Flight
    template_name = 'flight_list.html'
    context_object_name = 'flights'

    def get_queryset(self):
        source = self.kwargs['source']
        destination = self.kwargs['destination']
        return Flight.objects.filter(source=source, destination=destination, takeoff_time__gt=timezone.now())

class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flight_detail.html'
    context_object_name = 'flight'

    
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_form.html'

    def form_valid(self, form):
        form.instance.flight = get_object_or_404(Flight, pk=self.kwargs['pk'])
        booking = form.save()
        booking.booking_status = 'pending'
        booking.save()
        return redirect('booking-detail', pk=booking.pk)



class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'
    context_object_name = 'booking'


class EditBookingView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'edit_booking.html'
    context_object_name = 'booking'

    def get_success_url(self):
        return reverse_lazy('booking-detail', kwargs={'pk': self.object.pk})
    
class UpdateBookingStatusView(View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        new_status = request.POST.get('status')

        if new_status in ['confirmed', 'canceled']:
            booking.booking_status = new_status
            booking.save()
            return redirect('booking-detail', pk=booking.pk)
        return HttpResponseForbidden("Invalid action.")