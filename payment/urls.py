from django.urls import path
from .views import MyPaymentsAPIView

urlpatterns = [
    path('my/', MyPaymentsAPIView.as_view(), name='my-payments'),
]