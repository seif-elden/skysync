from django.contrib import admin
from .models import Plane , Flight , Booking

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




@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'passenger_name', 'passenger_passport', 'flight', 'number_of_seats', 'booking_status', 
        'booking_date', 'checked_in', 'luggage_count', 'total_price'
    )
    search_fields = ('passenger_name', 'passenger_passport', 'flight__flight_number', 'number_of_seats')
    list_filter = ('booking_status', 'checked_in', 'flight')

    readonly_fields = ('total_price',)

