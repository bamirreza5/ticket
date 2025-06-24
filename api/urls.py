from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/token/" , api_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/" , TokenRefreshView.as_view()),
    path("user/register/" , api_views.RegisterView.as_view()),
    path("user/password-rest-email/<email>/" , api_views.PasswordRestEmailVerifyAPIView.as_view()),
    path("user/password-change/" , api_views.PasswordChangeAPIView.as_view()),
    path("transport/", api_views.TransportListCreateAPIView.as_view(), name="transport-list-create"),
]