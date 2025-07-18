from django.db import models
from userauths.models import User
from booking.models import Booking

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'در انتظار'),
        ('completed', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]

    PAYMENT_METHOD = [
        ('card', 'کارت بانکی'),
        ('wallet', 'کیف پول'),
        ('paypal', 'پی‌پال'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='completed')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='card')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پرداخت {self.user.email} - {self.amount}"
