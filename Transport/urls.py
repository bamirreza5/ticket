from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path,include

schema_view = get_schema_view(
   openapi.Info(
      title="Ticket Reservation API",
      default_version='v1',
      description="API documentation for the ticket reservation system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('transport.urls')),
]