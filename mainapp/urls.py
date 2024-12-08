from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('flights/<str:source>/<str:destination>/', FlightListView.as_view(), name='flight-list'),
    path('flight/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('flight/<int:pk>/book/', BookingCreateView.as_view(), name='book-flight'),
    path('booking-detail/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('edit-booking/<int:pk>/', EditBookingView.as_view(), name='edit-booking'),
    path('update-booking-status/<int:pk>/', UpdateBookingStatusView.as_view(), name='update-booking-status'),

]
