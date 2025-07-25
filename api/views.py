from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from userauths.models import User,Profile
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from Transport.models import Transport
from api.serializer import TransportSerializer

from booking.models import Booking

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer

import random
def generate_random_otp(Length = 7):
    otp = ''.join([str(random.randint(0,9)) for _ in range(Length)])
    return otp
class PasswordRestEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.filter(email = email).first()

        if user:
             uuidb64 = user.pk
             refresh = RefreshToken.for_user(user)
             refresh_token = str(refresh.access_token)
              
             user.refresh_token = refresh_token
             user.otp = generate_random_otp()
             user.save()
             link = f"http://127.0.0.1:8000/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}"
             
            #  context = { 
            #      "link" : link,
            #      "username" : user.username,
            #  }
            #  subject = "Password Rest Email"
            #  text_body = render_to_string("email/password_reset.txt" , context)
            #  html_body = render_to_string("email/password_reset.html" , context)             
            #  msg = EmailMultiAlternatives(
            #     subject=subject,
            #     from_email=settings.FROM_EMAIL,
            #     to=[user.email],
            #     body=text_body
            # )
            #  msg.attach_alternative(html_body , "text/html")
            #  msg.send()
             
             print("link ======== " , link)
        return user

class PasswordChangeAPIView(generics.CreateAPIView):
    Permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def create(self,request , *args, **kwargs):
        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']

        user = User.objects.get(id=uuidb64 , otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response({"message " : "password change successfully"} , status=status.HTTP_201_CREATED)
        else: 
            return Response({"message " : "User Does not exists"} , status=status.HTTP_404_NOT_FOUND)

class TransportListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Transport.objects.all()
        params = self.request.query_params

        origin = params.get('origin')
        destination = params.get('destination')
        date = params.get('date')  # expected format: YYYY-MM-DD
        min_price = params.get('min_price')
        max_price = params.get('max_price')

        if origin:
            queryset = queryset.filter(origin__icontains=origin)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if date:
            queryset = queryset.filter(departure_time__date=date)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.order_by('departure_time')
    
    #http://127.0.0.1:8000/api/v1/transport/?origin=Iran&destination=germany
    #http://127.0.0.1:8000/api/v1/transport/?date=2025-07-01
    #http://127.0.0.1:8000/api/v1/transport/?min_price=200000&max_price=1000000
    #http://127.0.0.1:8000/api/v1/transport/?origin=Iran&destination=Germany&date=2025-07-05&min_price=300000&max_price=800000

from api.serializer import BookingSerializer
from booking.models import Booking

class BookTicketAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class MyBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class CancelBookingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)  # حذف شرط user

        # تست دسترسی
        if booking.user != request.user:
            return Response({"detail": "شما مالک این رزرو نیستید."}, status=403)

        booking.is_cancelled = True
        booking.save()
        return Response({"message": "رزرو با موفقیت لغو شد."}, status=status.HTTP_200_OK)

class CancelBookingBySeatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        seat_number = request.data.get("seat_number")
        transport_id = request.data.get("transport_id")

        if not seat_number or not transport_id:
            return Response({"error": "seat_number و transport_id الزامی هستند."}, status=400)

        try:
            booking = Booking.objects.get(
                seat_number=seat_number,
                transport_id=transport_id,
                user=request.user,
                is_cancelled=False
            )
        except Booking.DoesNotExist:
            return Response({"detail": "رزروی با این مشخصات برای شما یافت نشد."}, status=404)

        booking.is_cancelled = True
        booking.save()

        return Response({"message": "رزرو با موفقیت لغو شد."}, status=status.HTTP_200_OK)
    
    #example
    #     {
    #   "seat_number": 2,
    #   "transport_id": 1
    # }


class SeatAvailabilityAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, transport_id):
        transport = get_object_or_404(Transport, id=transport_id)
        total_seats = transport.total_seats

        booked_seats = Booking.objects.filter(
            transport=transport,
            is_cancelled=False
        ).values_list('seat_number', flat=True)
        booked_seats = set(map(int, booked_seats))

        seat_map = [
            {
                "seat_number": i,
                "is_booked": i in booked_seats
            } for i in range(1, total_seats + 1)
        ]

        return Response({
            "transport_id": transport.id,
            "total_seats": total_seats,
            "seats": seat_map
        })



from payment.models import Payment

class BookTicketAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        # استخراج مبلغ از مدل Transport
        amount = booking.transport.price

        # ایجاد پرداخت پس از رزرو
        Payment.objects.create(
            user=self.request.user,
            booking=booking,
            amount=amount,
            method='card',  # فرضی؛ اگر از فرم بخوای بگیری باید تغییر کنه
            status='completed'
        )
