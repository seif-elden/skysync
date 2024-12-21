from django import forms
from .models import Booking , passenger

class SearchFlightForm(forms.Form):
    source = forms.CharField(max_length=100, label="From")
    destination = forms.CharField(max_length=100, label="To")

class PassengerForm(forms.ModelForm):
    class Meta:
        model = passenger
        fields = ['name', 'passport', 'email', 'phone']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats', 'luggage_count']

    def save(self, commit=True):
        # Save Booking instance
        booking = super().save(commit=False)
        
        # Handle additional logic if required
        if commit:
            booking.save()
        return booking


class CombinedBookingForm(forms.Form):
    passenger_name = forms.CharField(max_length=100, help_text="Passenger's full name")
    passenger_passport = forms.CharField(max_length=50, help_text="Passenger's passport number")
    passenger_email = forms.EmailField(help_text="Passenger's email address")
    passenger_phone = forms.CharField(max_length=15, help_text="Passenger's contact phone number")
    number_of_seats = forms.IntegerField(min_value=1, help_text="Number of seats to book")
    luggage_count = forms.IntegerField(min_value=0, help_text="Number of luggage items")

    def save(self):
        # Create or update passenger
        passenger, created = passenger.objects.get_or_create(
            passport=self.cleaned_data['passenger_passport'],
            defaults={
                'name': self.cleaned_data['passenger_name'],
                'email': self.cleaned_data['passenger_email'],
                'phone': self.cleaned_data['passenger_phone']
            }
        )

        # Create booking
        booking = Booking(
            passenger=passenger,
            number_of_seats=self.cleaned_data['number_of_seats'],
            luggage_count=self.cleaned_data['luggage_count']
        )
        booking.save()
        return booking

