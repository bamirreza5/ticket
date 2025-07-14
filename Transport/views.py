from rest_framework import generics, permissions, filters
from .models import Transport
from .serializer import TransportSerializer


class TransportListCreateView(generics.ListCreateAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['origin', 'destination']
    ordering_fields = ['departure_time', 'price']

    def get_permissions(self):
        # فقط ادمین اجازه اضافه کردن داره
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]