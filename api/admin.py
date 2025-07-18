from django.contrib import admin
from booking.models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'transport', 'seat_number', 'booking_date'] 
    list_filter = ['transport', 'booking_date'] 
    search_fields = ['user__username', 'transport__origin', 'transport__destination', 'seat_number']
    ordering = ['-booking_date']  