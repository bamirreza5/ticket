from rest_framework import generics, permissions
from .models import Payment
from .serializers import PaymentSerializer

class MyPaymentsAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-paid_at')
