from django.contrib import admin
from .models import Transport

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('transport_type', 'origin', 'destination', 'departure_time', 'arrival_time', 'price')