from django import forms
from .models import Booking

class SearchFlightForm(forms.Form):
    source = forms.CharField(max_length=100, label="From")
    destination = forms.CharField(max_length=100, label="To")

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'passenger_name', 'passenger_passport', 'passenger_email', 
            'passenger_phone', 'number_of_seats', 'luggage_count' 
        ]


