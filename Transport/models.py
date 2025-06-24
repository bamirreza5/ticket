from django.db import models

class Transport(models.Model):
    TRANSPORT_TYPE_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPE_CHOICES)
    origin = models.CharField(max_length=100)             
    destination = models.CharField(max_length=100)        
    departure_time = models.DateTimeField()               
    arrival_time = models.DateTimeField()                
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.transport_type} | {self.origin} → {self.destination} | {self.departure_time.strftime('%Y-%m-%d %H:%M')}"
