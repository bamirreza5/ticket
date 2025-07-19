from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from Transport.models import Transport

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False, editable=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['transport', 'seat_number'],
                condition=models.Q(is_cancelled=False),
                name='unique_active_booking'
            )
        ]
    def __str__(self):
        return f"{self.user.email} - {self.transport} - Seat {self.seat_number}"
