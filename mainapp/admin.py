from django.contrib import admin
from .models import Plane , Flight , Booking , passenger

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('model', 'serial_number', 'status', 'manufacture_date', 'last_maintenance_date', 'flight_hours')
    search_fields = ('model', 'serial_number')
    list_filter = ('status',)



@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'flight_number', 'plane', 'source', 'destination', 'takeoff_time', 'landing_time', 
        'pilot_name', 'crew_count', 'ticket_price', 'available_seats', 'status'
    )
    search_fields = ('flight_number', 'source', 'destination', 'plane__model', 'pilot_name')
    list_filter = ('status', 'source', 'destination', 'takeoff_time', 'landing_time')
    
    readonly_fields = ('available_seats',)


@admin.register(passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'passport', 'email', 'phone')  # Display these fields in the admin list view
    search_fields = ('name', 'passport', 'email')  # Enable search by these fields
    list_filter = ('email',)  # Filter passengers by email domain if needed


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('flight', 'passenger', 'number_of_seats', 'booking_status', 'booking_date')
    search_fields = ('passenger__name', 'flight__flight_number')
    list_filter = ('booking_status', 'booking_date')
