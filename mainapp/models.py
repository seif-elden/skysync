from django.db import models
from django.utils import timezone
from datetime import timedelta


class Plane(models.Model):
    PLANE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]

    model = models.CharField(max_length=100, help_text="Model of the plane")
    manufacture_date = models.DateField(help_text="Date when the plane was manufactured")
    status = models.CharField(
        max_length=20,
        choices=PLANE_STATUS_CHOICES,
        default='active',
        help_text="Current status of the plane",
    )
    number_of_seats = models.PositiveIntegerField(help_text="Total number of seats in the plane")
    serial_number = models.CharField(max_length=50, unique=True, help_text="Unique serial number of the plane")
    last_maintenance_date = models.DateField(null=True, blank=True, help_text="Date of last maintenance")
    flight_hours = models.PositiveIntegerField(default=0, help_text="Total flight hours the plane has completed")
    fuel_capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fuel capacity in liters")
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight of the plane in kilograms")

    def __str__(self):
        return f"{self.model} - {self.serial_number}"



class Flight(models.Model):
    FLIGHT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('delayed', 'Delayed'),
        ('in_flight', 'In Flight'),
        ('landed', 'Landed'),
        ('canceled', 'Canceled'),
    ]

    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='flights')
    flight_number = models.CharField(max_length=20, unique=True, help_text="Unique flight number")
    source = models.CharField(max_length=100, help_text="The starting point of the flight")
    destination = models.CharField(max_length=100, help_text="The destination of the flight")
    takeoff_time = models.DateTimeField(help_text="Time when the flight is scheduled to take off")
    landing_time = models.DateTimeField(help_text="Time when the flight is scheduled to land")
    pilot_name = models.CharField(max_length=100, help_text="Name of the pilot in charge of the flight")
    crew_count = models.PositiveIntegerField(default=5, help_text="Number of crew members on board")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price of a ticket in USD")
    available_seats = models.PositiveIntegerField(help_text="Total number of available seats for this flight")
    status = models.CharField(
        max_length=15,
        choices=FLIGHT_STATUS_CHOICES,
        default='scheduled',
        help_text="Current status of the flight"
    )

    def __str__(self):
        return f"Flight {self.flight_number} from {self.source} to {self.destination} - Plane: {self.plane.model}"

    def save(self, *args, **kwargs):
        # If available_seats is not set (or set to 0), default it to the number of seats in the plane
        if not self.available_seats:
            self.available_seats = self.plane.number_of_seats


        # If the flight has landed and the status has just changed to 'landed'
        if self.status == 'landed' and self.pk:
            # Calculate flight duration in hours (between takeoff and landing)
            flight_duration = self.landing_time - self.takeoff_time
            flight_duration_hours = flight_duration.total_seconds() / 3600  # Convert to hours
            
            # Add flight duration to the plane's total flight hours
            self.plane.flight_hours += flight_duration_hours
            self.plane.save()

        super().save(*args, **kwargs)

    def is_upcoming(self):
        """Check if the flight is scheduled for a future time."""
        return self.takeoff_time > timezone.now()

    def has_landed(self):
        """Check if the flight has already landed."""
        return self.landing_time < timezone.now()


class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('pending', 'Pending'),
    ]

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    passenger_name = models.CharField(max_length=100, help_text="Passenger's full name")
    passenger_passport = models.CharField(max_length=50, help_text="Passenger's passport number")
    passenger_email = models.EmailField(help_text="Passenger's email address")
    passenger_phone = models.CharField(max_length=15, help_text="Passenger's contact phone number")
    number_of_seats = models.PositiveIntegerField(help_text="Assigned seat number",null=True)
    booking_status = models.CharField(
        max_length=10,
        choices=BOOKING_STATUS_CHOICES,
        default='pending',
        help_text="Current status of the booking"
    )
    booking_date = models.DateTimeField(default=timezone.now, help_text="Date and time when the booking was made")
    checked_in = models.BooleanField(default=False, help_text="Has the passenger checked in?")
    luggage_count = models.PositiveIntegerField(default=0, help_text="Number of luggage items")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Total price of the booking in USD")
    
    def __str__(self):
        return f"Booking for {self.passenger_name} on flight {self.flight.flight_number}"

    def save(self, *args, **kwargs):
        # Automatically assign the price to match the flight's ticket price
        self.total_price = self.flight.ticket_price * self.number_of_seats 

        # If the booking is confirmed and the status has changed to 'confirmed'
        if self.booking_status == 'confirmed':
            # Decrease the available seats for the flight
            if self.flight.available_seats > 0:
                self.flight.available_seats -= self.number_of_seats
                self.flight.save()
            else:
                raise ValueError("No available seats left on this flight.")
        
        super().save(*args, **kwargs)

    def is_confirmed(self):
        """Check if the booking is confirmed."""
        return self.booking_status == 'confirmed'
