from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

urlpatterns = [
    path("user/token/" , api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/" , TokenRefreshView.as_view()),
    path("user/register/" , api_views.RegisterView.as_view()),
    path("user/password-rest/<email>/" , api_views.PasswordRestEmailVerifyAPIView.as_view()),
    path("user/password-change/" , api_views.PasswordChangeAPIView.as_view()),
    path("transport/", api_views.TransportListCreateAPIView.as_view(), name="transport-list-create"),
    path("bookings/", api_views.BookTicketAPIView.as_view(), name="book-ticket"),
    path("my-bookings/", api_views.MyBookingsAPIView.as_view(), name="my-bookings"),
    path("cancel-booking/<int:booking_id>/", api_views.CancelBookingAPIView.as_view(), name="cancel-booking"),
    path('api-auth/', include('rest_framework.urls')),
    path("transport/<int:transport_id>/seats/", api_views.SeatAvailabilityAPIView.as_view(), name="seat-availability"),
    path('payments/', include('payment.urls')),
    path("cancel-booking-by-seat/", api_views.CancelBookingBySeatAPIView.as_view(), name="cancel-booking-by-seat"),
]